from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, noload
from sqlalchemy import select

from src import models, schemas, exceptions, utils


def create_customer(db: Session, customer: schemas.CustomerCreateInput):
    customer.password = utils.get_password_hash(customer.password)
    db_customer = models.Customer(**customer.dict())

    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error creating customer")

    return db_customer


def get_customer_by_id(db: Session, id: str) -> models.Customer:
    query = select(models.Customer).where(models.Customer.id == id)
    customer = db.execute(query).scalar()
    return customer


def get_customer_by_mail(db: Session, mail: str) -> models.Customer:
    query = select(models.Customer).where(models.Customer.mail == mail)
    customer = db.execute(query).scalar()
    return customer


def get_all_customers(db: Session):
    query = select(models.Customer).options(noload(models.Customer.orders))
    customers = db.execute(query).scalars().all()
    return customers


def update_customer(
    db: Session, update_data: schemas.CustomerUpdateInput, customer: models.Customer
) -> models.Customer:
    update_data: dict = update_data.dict(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    try:
        db.commit()
        db.refresh(customer)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error updating customer")

    return customer


def delete_customer(db: Session, customer: models.Customer):
    try:
        db.delete(customer)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error deleting customer")


def create_item(db: Session, item: schemas.ItemCreateInput):
    db_item = models.Item(**item.dict())

    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error creating item")

    return db_item


def get_item_by_id(db: Session, id: str) -> models.Item:
    query = select(models.Item).where(models.Item.id == id)
    item = db.execute(query).scalar()
    return item


def get_lock_item_by_id(db: Session, id: str) -> models.Item:
    query = select(models.Item).where(models.Item.id == id).with_for_update()
    item = db.execute(query).scalar()
    return item


def get_item_by_name(db: Session, name: str) -> models.Item:
    query = select(models.Item).where(models.Item.item_name == name)
    item = db.execute(query).scalar()
    return item


async def get_all_items(db: AsyncSession):
    query = select(models.Item)
    result = await db.execute(query)
    items = result.scalars().all()
    return items


def update_item(
    db: Session, update_data: schemas.ItemUpdateInput, item: models.Item
) -> models.Item:
    update_data: dict = update_data.dict(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    try:
        db.commit()
        db.refresh(item)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error updating item")

    return item


def delete_item(db: Session, item: models.Item):
    try:
        db.delete(item)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error deleting item")


def create_order(
    db: Session, item: models.Item, order: schemas.OrderCreateInput, customer_id: str
):
    db_order = models.Order(**order.dict())
    db_order.customer_id = customer_id
    item.quantity -= order.quantity

    db.add(db_order)
    try:
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error creating order")

    return db_order
