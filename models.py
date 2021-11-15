from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Expense(Base):
    """
    Table to store expenses
    """

    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"Expense: {self.price}"


class Category(Base):
    """
    Table to store categories of expenses
    """

    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    expenses = relationship("Expense", back_populates="category")

    def __repr__(self):
        return f"Category: {self.title}"


class User(Base):
    """
    Table to store users of app
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    expenses = relationship("Expense", back_populates="user")

    def __repr__(self):
        return f"ID: {self.user_id}\tUsername: {self.username}"
