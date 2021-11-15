import getpass

from commands import switch, show_commands
from service import (
    user_insert,
    expense_insert,
    category_insert,
    get_user,
    get_expenses_by_params,
    get_categories,
)
from setup_db import setup_database


def main():
    show_commands()
    session = setup_database("sqlite.db")
    user_input = switch()
    if user_input == "register":
        register(session)
    elif user_input == "create expense":
        create_expense(session)
    elif user_input == "create expense by day":
        create_expense(session, by_date=True)
    elif user_input == "get all expenses":
        get_expenses(session)
    elif user_input == "get expenses by category":
        get_categories(session)
        category_id = input("Write id of the category: ")
        get_expenses(session, category_id=category_id)
    elif user_input == "get expenses by year":
        year = int(input("Write the year you want to get expenses by: "))
        get_expenses(session, year=year)
    elif user_input == "get expenses by month":
        month_year = input(
            "Write the month you want to get expenses by in format 'month.year': "
        ).split(".")
        month, year = list(map(int, month_year))
        get_expenses(session, year=year, month=month)
    elif user_input == "get expenses by day":
        day_month_year = input(
            "Write the day you want to get expenses by in format 'day.month.year': "
        ).split(".")
        day, month, year = list(map(int, day_month_year))
        get_expenses(session, year=year, month=month, day=day)
    elif user_input == "delete all expenses":
        delete_all_expenses(session)
    elif user_input == "incorrect":
        print("Incorrect command")
    return None


def register(session):
    username = input("Write your new username: ")
    password1 = getpass.getpass()
    password2 = getpass.getpass("Password verification: ")
    user_insert(session, username, password1, password2)
    return None


def create_expense(session, by_date=False):
    user = auth_user(session)
    if user:
        if by_date:
            expense_input = input(
                "You expense in format: \nyear.month.day category-price\n20.11.2021 еда-500\n"
            )
            expense_date, expense_info = expense_input.split(" ")
            day_month_year = expense_date.split(".")
            day, month, year = list(map(int, day_month_year))
            category_title, price = expense_info.split("-")
            category = category_insert(session, category_title)
            expense_insert(
                session, category.category_id, user.user_id, price, year, month, day
            )
        else:
            expense_input = input("You expense in format: \ncategory-price\nеда-500\n")
            category_title, price = expense_input.split("-")
            category = category_insert(session, category_title)
            expense_insert(session, category.category_id, user.user_id, price)
            return None
    else:
        print("Your credentials are not valid")
        return None


def get_expenses(session, category_id=None, year=None, month=None, day=None):
    user = auth_user(session)
    if user:
        expenses = get_expenses_by_params(
            session, user.user_id, category_id, year, month, day
        )
        if expenses:
            summary = 0
            print("CATEGORY TITLE\t\tEXPENSE\t\tEXPENSE TIMESTAMP")
            for expense in expenses:
                print(
                    f"{expense.category.title:22}{expense.price:6}\t\t{expense.timestamp}"
                )
                summary += expense.price
            print(f"The sum of the expenses: {summary}")
            return None
    else:
        print("Your credentials are not valid")
        return None


def delete_all_expenses(session):
    user = auth_user(session)
    get_expenses_by_params(session, user_id=user.user_id).delete()
    session.commit()
    print("You data is deleted")
    return None


def auth_user(session):
    username = input("Write your username: ")
    password = getpass.getpass()
    user = get_user(session, username, password)
    return user if user else None


if __name__ == "__main__":
    main()
