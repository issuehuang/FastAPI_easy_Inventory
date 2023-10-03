from fastapi import Depends
from sqlalchemy.orm import Session

from src import models, schemas, exceptions, utils, service, jwt
from src.config import ADMIN_USERNAME, ADMIN_PASSWORD
from src.database import get_db


def check_new_customer(
    customer: schemas.CustomerCreateInput, db: Session = Depends(get_db)
) -> tuple[schemas.CustomerCreateInput, Session]:
    db_customer = service.get_customer_by_mail(db, customer.mail)
    if db_customer:
        raise exceptions.CustomerAlreadyExists()
    return customer, db


def authenticate_customer(
    data: schemas.LoginInput, db: Session = Depends(get_db)
) -> models.Customer:
    db_customer = service.get_customer_by_mail(db, data.username)
    if not db_customer:
        raise exceptions.CustomerNotFound()
    if not utils.verify_password(data.password, db_customer.password):
        raise exceptions.InvalidPasswordOrEmail()
    return db_customer


def authenticate_admin(data: schemas.LoginInput) -> bool:
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise exceptions.InvalidPasswordOrEmail()
    return True


def check_new_item(
    item: schemas.ItemCreateInput, db: Session = Depends(get_db)
) -> tuple[schemas.ItemCreateInput, Session]:
    db_item = service.get_item_by_name(db, item.item_name)
    if db_item:
        raise exceptions.ItemAlreadyExists()
    return item, db


def check_is_admin(jwt_data: dict = Depends(jwt.decode_jwt)) -> None:
    if jwt_data['sub'] != 'admin':
        raise exceptions.NotAdmin()


def check_item_enough_quantity(
    order: schemas.OrderCreateInput, db: Session = Depends(get_db)
) -> tuple[models.Item, schemas.OrderCreateInput, Session]:
    item = service.get_lock_item_by_id(db, order.item_id)
    if not item:
        raise exceptions.ItemNotFound()
    if item.quantity < order.quantity:
        raise exceptions.ItemNotEnoughQuantity()
    return item, order, db
