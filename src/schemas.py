from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional


class DateTimeBase(BaseModel):
    created_at: str
    updated_at: str

    @validator("created_at", "updated_at", pre=True)
    def datetime_to_str(cls, v: datetime):
        if isinstance(v, datetime):
            return datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
        return str(v)


class Customer(DateTimeBase):
    id: str
    customer_name: str

    class Config:
        orm_mode = True


class CustomerCreateInput(BaseModel):
    customer_name: str = Field(max_length=30, title="Customer name")
    mail: EmailStr
    password: str = Field(max_length=64, title="Password")


class CustomerUpdateInput(BaseModel):
    customer_name: Optional[str] = Field(max_length=30, title="Customer name")


class LoginInput(BaseModel):
    username: Optional[EmailStr]
    password: Optional[str] = Field(max_length=30, title="Password")


class LoginReturn(Customer):
    token: str


class ItemBase(DateTimeBase):
    id: str
    item_name: str
    price: float
    quantity: int

    class Config:
        orm_mode = True


class ItemCreateInput(BaseModel):
    item_name: str
    price: float
    quantity: int


class ItemUpdateInput(BaseModel):
    item_name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class OrderBase(DateTimeBase):
    id: str
    customer_id: str
    item_id: str
    quantity: int

    class Config:
        orm_mode = True


class OrderCreateInput(BaseModel):
    item_id: str
    quantity: int
