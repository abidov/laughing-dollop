def register_command():
    return "register"


def get_expenses_by_category_command():
    return "get expenses by category"


def get_all_expenses_command():
    return "get all expenses"


def get_expenses_by_year_command():
    return "get expenses by year"


def get_expenses_by_month_command():
    return "get expenses by month"


def get_expenses_by_day_command():
    return "get expenses by day"


def create_expense_command():
    return "create expense"


def create_expense_by_day_command():
    return "create expense by day"


def delete_all_expenses_command():
    return "delete all expenses"


def default_command():
    return "incorrect"


switcher = {
    "register": register_command,
    "create expense": create_expense_command,
    "create expense by day": create_expense_by_day_command,
    "get all expenses": get_all_expenses_command,
    "get expenses by category": get_expenses_by_category_command,
    "get expenses by year": get_expenses_by_year_command,
    "get expenses by month": get_expenses_by_month_command,
    "get expenses by day": get_expenses_by_day_command,
    "delete all expenses": delete_all_expenses_command,
}


def switch():
    command = input("Write your command: ")
    return switcher.get(command, default_command)()


def show_commands():
    commands = switcher.keys()
    print("All commands in this app: ")
    for command in commands:
        print(command)
    return None
