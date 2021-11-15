import unittest

from models import User, Expense, Category
from setup_db import setup_database
from service import (
    category_insert,
    user_insert,
    expense_insert,
    get_user,
    get_category,
    get_categories,
    get_expenses_by_year,
    get_expenses_by_month,
    get_expenses_by_day,
    get_expenses_by_category,
    get_expenses_of_user,
)


class TestInsertMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.session = setup_database("test_insert.db")

    def tearDown(self) -> None:
        self.session.query(User).delete()
        self.session.query(Expense).delete()
        self.session.query(Category).delete()
        self.session.commit()

    def test_user_insert(self):
        user = user_insert(self.session, "test", "Pass", "Pass")
        self.assertEqual(user.username, "test")

    def test_category_insert(self):
        category = category_insert(self.session, category_title="taxi")
        self.assertEqual(category.title, "TAXI")

    def test_expense_insert(self):
        user = user_insert(self.session, "arslan", "pass", "pass")
        category = category_insert(self.session, "food")
        expense = expense_insert(self.session, category.category_id, user.user_id, 2000)
        self.assertEqual(expense.price, 2000)


class TestGetMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.session = setup_database("test_get.db")
        self.category = category_insert(self.session, "taxi")
        self.user = user_insert(self.session, "arslan", "pass", "pass")
        self.expense = expense_insert(
            self.session,
            self.category.category_id,
            self.user.user_id,
            price=2000,
            year=2020,
            month=5,
            day=10,
        )

    def tearDown(self) -> None:
        self.session.query(User).delete()
        self.session.query(Expense).delete()
        self.session.query(Category).delete()
        self.session.commit()

    def test_get_user(self):
        user1 = get_user(self.session, "arslan", "pass")
        user2 = get_user(self.session, "arslan2", "pass")
        self.assertEqual(user1, self.user)
        self.assertIsNone(user2)

    def test_get_category(self):
        category1 = get_category(self.session, "TAXI")
        category2 = get_category(self.session, "FOOD")
        self.assertEqual(category1, self.category)
        self.assertIsNone(category2)

    def test_get_categories(self):
        categories1 = get_categories(self.session)
        self.assertEqual(categories1, [self.category])
        self.session.query(Category).delete()
        categories2 = get_categories(self.session)
        self.assertEqual(categories2, [])

    def test_get_expenses_by_year(self):
        expenses1 = [
            expense
            for expense in get_expenses_by_year(self.session, self.user.user_id, 2020)
        ]
        expenses2 = [
            expense
            for expense in get_expenses_by_year(self.session, self.user.user_id, 2021)
        ]
        self.assertEqual(expenses1, [self.expense])
        self.assertEqual(expenses2, [])

    def test_get_expenses_by_month(self):
        expenses1 = [
            expense
            for expense in get_expenses_by_month(
                self.session, self.user.user_id, 2020, 5
            )
        ]
        expenses2 = [
            expense
            for expense in get_expenses_by_month(
                self.session, self.user.user_id, 2021, 5
            )
        ]
        self.assertEqual(expenses1, [self.expense])
        self.assertEqual(expenses2, [])

    def test_get_expenses_by_day(self):
        expenses1 = [
            expense
            for expense in get_expenses_by_day(
                self.session, self.user.user_id, 2020, 5, 10
            )
        ]
        expenses2 = [
            expense
            for expense in get_expenses_by_day(
                self.session, self.user.user_id, 2021, 5, 10
            )
        ]
        self.assertEqual(expenses1, [self.expense])
        self.assertEqual(expenses2, [])

    def test_get_expenses_by_category(self):
        expenses1 = [
            expense
            for expense in get_expenses_by_category(
                self.session, self.user.user_id, self.category.category_id
            )
        ]
        expenses2 = [
            expense
            for expense in get_expenses_by_category(self.session, self.user.user_id, 10)
        ]
        self.assertEqual(expenses1, [self.expense])
        self.assertEqual(expenses2, [])

    def test_get_expenses_of_user(self):
        expenses1 = [
            expense for expense in get_expenses_of_user(self.session, self.user.user_id)
        ]
        expenses2 = [expense for expense in get_expenses_of_user(self.session, 10)]
        self.assertEqual(expenses1, [self.expense])
        self.assertEqual(expenses2, [])


if __name__ == "__main__":
    unittest.main()
