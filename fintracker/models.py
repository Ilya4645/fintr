from datetime import datetime

"""
Модуль models - определяет классы Transaction, Expense, Income и их аргументы.
"""
class Transaction:
    """Базовый класс для транзакций (доход/расход)."""
    def __init__(self, description: str, amount: float, date: datetime = None):
        """Инициализирует новый объект Transaction.

        Args:
            description(str): Описание транзакции.
            amount(float): Сумма транзакции.
            date(datetime): Дата соверешения транзакции.

        Raises:
            ValueError: Если ввести пустую строку или отрицательное число.
        """
        if not isinstance(description, str) or not description:
            raise ValueError("Описание должно быть непустой строкой.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сумма должна быть положительным числом.")

        self.description = description
        self.amount = amount
        self.date = date if date else datetime.now()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.description}, {self.amount:.2f}, {self.date.strftime('%Y-%m-%d %H:%M:%S')}>"

class Expense(Transaction):
    """Представляет собой расход. Наследован от базового класса Transaction"""
    def __init__(self, description: str, amount: float, category: str, date: datetime = None):
        """Инициализирует новый объект Expense.

        Args:
            description(str): Описание транзакции.
            amount(float): Сумма транзакции.
            date(datetime): Дата соверешения транзакции.
            category(str): Категория расхода.

        Raises:
            ValueError: Если ввести пустую строку.
        """
        super().__init__(description, amount, date)
        if not isinstance(category, str) or not category:
            raise ValueError("Категория должна быть непустой строкой.")
        self.category = category

    def __repr__(self):
        return f"<Expense: {self.description}, {self.amount:.2f}, Category: {self.category}, Date: {self.date.strftime('%Y-%m-%d')}>"

class Income(Transaction):
    """Представляет собой доход. Наследован от базового класса Transaction"""
    def __init__(self, description: str, amount: float, source: str, date: datetime = None):
        """Инициализирует новый объект Expense.

        Args:
            description(str): Описание транзакции.
            amount(float): Сумма транзакции.
            date(datetime): Дата соверешения транзакции.
            source(str): Источник дохода.

        Raises:
            ValueError: Если ввести пустую строку.
        """
        super().__init__(description, amount, date)
        if not isinstance(source, str) or not source:
            raise ValueError("Источник должно быть непустой строкой.")
        self.source = source

    def __repr__(self):
        return f"<Income: {self.description}, {self.amount:.2f}, Source: {self.source}, Date: {self.date.strftime('%Y-%m-%d')}>"
