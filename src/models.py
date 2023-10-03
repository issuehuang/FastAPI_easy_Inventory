from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import mapped_column, relationship

from src.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_name = mapped_column(String(30))
    mail = mapped_column(String(100))
    password = mapped_column(String(64))
    orders = relationship("Order", back_populates="customer", lazy="joined")


class Order(Base):
    __tablename__ = "orders"

    customer_id = mapped_column(String, ForeignKey("customers.id"), index=True)
    item_id = mapped_column(String, ForeignKey("items.id"), index=True)
    quantity = mapped_column(Integer, default=1)
    customer = relationship("Customer", back_populates="orders")
    item = relationship("Item", lazy="joined")


class Item(Base):
    __tablename__ = "items"

    item_name = mapped_column(String(30))
    price = mapped_column(Float, default=0.0)
    quantity = mapped_column(Integer, default=0)
