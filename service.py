import bcrypt

from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from models import User, Category, Expense


def category_insert(session, category_title):
    """
    Function to create category
    :param session:
    :param category_title:
    :return: returns created category
    """
    category = Category(title=category_title.upper())
    session.add(category)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        category = get_category(session, category_title=category_title)
    print(f"New category created with title: {category_title}")
    return category


def expense_insert(
    session, category_id, user_id, price, year=None, month=None, day=None
):
    """
    Function to create expense
    :param day: day
    :param month: month
    :param year: year
    :param session: current db session
    :param category_id: category id
    :param user_id: user id
    :param price: price of expense
    :return: returns created expense
    """
    if year and month and day:
        expense_date = datetime(year, month, day)
        expense = Expense(
            category_id=category_id,
            user_id=user_id,
            price=price,
            timestamp=expense_date,
        )
    else:
        expense = Expense(category_id=category_id, user_id=user_id, price=price)
    session.add(expense)
    session.commit()
    print("Expense inserted")
    return expense


def user_insert(session, username, password1, password2):
    """
    Function to create user
    :param session: current db session
    :param username: username
    :param password1: password
    :param password2: password to verify
    :return: returns user if password verified and no user with same username
    """
    password = verify_password(password1, password2)
    if password:
        user = User(username=username, password=password)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Username already taken. Please try other username.")
        else:
            print(f"User was created with username {username}")
            return user
    else:
        print("Your passwords is not matching.")


def verify_password(password1, password2):
    """
    Password verification function
    :return: hashed password if verified else None
    """
    if password1 == password2:
        return bcrypt.hashpw(password1.encode("utf-8"), bcrypt.gensalt())
    return None


def get_user(session, username, password):
    """
    Private function to get users
    :param session: current db session
    :param username: username
    :param password: password
    :return: user if found, else None
    """
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password):
        return user
    return None


def get_category(session, category_title=None, category_id=None):
    """
    Function to get category by id or title
    :param session: current db session
    :param category_title: category title
    :param category_id: cateogry id
    :return: category or None if does not exist
    """
    category = None
    if category_title:
        category = session.query(Category).filter_by(title=category_title).first()
    elif category_id:
        category = session.query(Category).filter_by(category_id=category_id).first()
    return category


def get_categories(session):
    """
    Function to get all categories
    :param session: current db session
    :return: category list
    """
    print("ID\tCATEGORY TITLE")
    categories = session.query(Category).all()
    for category in categories:
        print(f"{category.category_id}\t{category.title}")
    return categories


def get_expenses_by_params(
    session, user_id, category_id=None, year=None, month=None, day=None
):
    """
    Function to get expenses by some params
    :param session: current db session
    :param user_id: user id
    :param category_id: category id
    :param year: year
    :param month: month
    :param day: day
    :return: returns list of expenses
    """
    if year and not month and not day:
        expenses = get_expenses_by_year(session, user_id, year)
    elif year and month and not day:
        expenses = get_expenses_by_month(session, user_id, year, month)
    elif year and month and day:
        expenses = get_expenses_by_day(session, user_id, year, month, day)
    elif category_id:
        expenses = get_expenses_by_category(session, user_id, category_id)
    else:
        expenses = get_expenses_of_user(session, user_id)
    return expenses


def get_expenses_by_year(session, user_id, year):
    """
    Function to get expenses by year
    :param session: current db session
    :param user_id: user id
    :param year: year
    :return: returns list of expenses
    """
    date_begin = datetime(year=year, month=1, day=1)
    date_end = datetime(year=year + 1, month=1, day=1)
    expenses = (
        session.query(Expense)
        .filter_by(user_id=user_id)
        .filter(and_(Expense.timestamp >= date_begin, Expense.timestamp < date_end))
    )
    return expenses


def get_expenses_by_month(session, user_id, year, month):
    """
    Function to get expenses by month
    :param session: current db session
    :param user_id: user id
    :param year: year
    :param month: month
    :return: returns list of expenses
    """
    date_begin = datetime(year=year, month=month, day=1)
    date_end = datetime(year=year, month=month + 1, day=1)
    expenses = (
        session.query(Expense)
        .filter_by(user_id=user_id)
        .filter(and_(Expense.timestamp >= date_begin, Expense.timestamp < date_end))
    )
    return expenses


def get_expenses_by_day(session, user_id, year, month, day):
    """
    Function to get expenses by day
    :param session: current db session
    :param user_id: user id
    :param year: year
    :param month: month
    :param day: day
    :return: returns list of expenses
    """
    date_begin = datetime(year=year, month=month, day=day)
    date_end = datetime(year=year, month=month, day=day + 1)
    expenses = (
        session.query(Expense)
        .filter_by(user_id=user_id)
        .filter(and_(Expense.timestamp >= date_begin, Expense.timestamp < date_end))
    )
    return expenses


def get_expenses_by_category(session, user_id, category_id):
    """
    Function to get expenses by category
    :param session: current db session
    :param user_id: user id
    :param category_id: category id
    :return: returns list of expenses
    """
    expenses = session.query(Expense).filter_by(
        user_id=user_id, category_id=category_id
    )
    return expenses


def get_expenses_of_user(session, user_id):
    """
    Function to get all expenses of user
    :param session: current db session
    :param user_id: user id
    :return: returns list of expenses
    """
    expenses = session.query(Expense).filter_by(user_id=user_id)
    return expenses
