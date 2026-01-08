import argparse
from datetime import datetime
from fintracker.models import Expense, Income
from fintracker.storage import add_expense

def add_command(args):
    """Обработчик команды --add."""
    try:
        transaction_date = None
        if args.date:
            transaction_date = datetime.strptime(args.date, '%Y-%m-%d')

        if args.expense: # Добавление расхода
            expense = Expense(description=args.description, amount=args.sum, category=args.category, date=transaction_date)
            add_expense(expense)
            print(f"Добавлен расход: {expense}")
        elif args.income: # Добавление дохода
            income = Income(description=args.description, amount=args.sum, source=args.source, date=transaction_date)
            add_expense(income)
            print(f"Добавлен доход: {income}")
        else:
            print("Необходимо указать --expense или --income для добавления транзакции.")

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except Exception as e:
        print(f"Произошла ошибка при добавлении транзакции: {e}")
