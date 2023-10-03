from fastapi import FastAPI, status, Depends, Response, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src import dependencies, schemas, service, exceptions, models, jwt, mail
from src.database import get_db

from uuid import UUID


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("3/5 second")
def root(request: Request):
    """
    Root
    """
    return {"message": "Hello World"}


@app.post(
    "/customers",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Customer,
)
def create_customer(dependency=Depends(dependencies.check_new_customer)):
    """
    Create a customer
    """
    customer, db = dependency
    return service.create_customer(db, customer)


@app.get(
    "/customers",
    response_model=schemas.Customer,
    responses={404: {"description": "Customer not found"}},
)
def get_customer_by_id(
    jwt_data: dict = Depends(jwt.decode_jwt), db: Session = Depends(get_db)
):
    """
    Get a customer by id
    """
    id = jwt_data["sub"]
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return customer


@app.post("/login", response_model=schemas.LoginReturn)
def login(
    response: Response,
    customer: models.Customer = Depends(dependencies.authenticate_customer),
):
    """
    Login
    """
    access_token = jwt.create_access_token(
        data={"sub": customer.id, "mail": customer.mail}
    )
    customer.token = access_token
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return customer


@app.post(
    "/admin/login",
    response_model=str,
    dependencies=[Depends(dependencies.authenticate_admin)],
)
def admin_login(response: Response):
    """
    Admin Login
    """
    access_token = jwt.create_access_token(data={"sub": "admin"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token


@app.patch(
    "/customers",
    response_model=schemas.Customer,
    responses={404: {"description": "Customer not found"}},
)
def update_customer(
    id: UUID, update_data: schemas.CustomerUpdateInput, db: Session = Depends(get_db)
):
    """
    Update a customer
    """
    id = str(id)
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return service.update_customer(db, update_data, customer)


@app.delete(
    "/customers",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Customer not found"}},
)
def delete_customer(id: UUID, db: Session = Depends(get_db)):
    """
    Delete a customer
    """
    id = str(id)
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    service.delete_customer(db, customer)


@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ItemBase,
    dependencies=[Depends(dependencies.check_is_admin)],
)
def create_item(dependency=Depends(dependencies.check_new_item)):
    """
    Create an item
    """
    item, db = dependency
    return service.create_item(db, item)


@app.get(
    "/items",
    response_model=list[schemas.ItemBase],
    dependencies=[Depends(dependencies.check_is_admin)],
)
async def get_items(db: AsyncSession = Depends(get_db)):
    """
    Get all items
    """
    return await service.get_all_items(db)


@app.patch(
    "/items",
    response_model=schemas.ItemBase,
    dependencies=[Depends(dependencies.check_is_admin)],
    responses={404: {"description": "Item not found"}},
)
def update_item(
    id: UUID, update_data: schemas.ItemUpdateInput, db: Session = Depends(get_db)
):
    """
    Update an item
    """
    id = str(id)
    item = service.get_item_by_id(db, id)
    if not item:
        raise exceptions.ItemNotFound()
    return service.update_item(db, update_data, item)


@app.delete(
    "/items",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(dependencies.check_is_admin)],
    responses={404: {"description": "Item not found"}},
)
def delete_item(id: UUID, db: Session = Depends(get_db)):
    """
    Delete an item
    """
    id = str(id)
    item = service.get_item_by_id(db, id)
    if not item:
        raise exceptions.ItemNotFound()
    service.delete_item(db, item)


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrderBase,
)
def create_order(
    background_tasks: BackgroundTasks,
    jwt_data: dict = Depends(jwt.decode_jwt),
    dependency=Depends(dependencies.check_item_enough_quantity),
):
    """
    Create an order
    """
    item, order, db = dependency
    customer_id = jwt_data["sub"]
    order = service.create_order(db, item, order, customer_id)
    background_tasks.add_task(mail.fake_send_mail, f"Order {order.id} created")
    return order
