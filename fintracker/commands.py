import argparse
from datetime import datetime, timedelta, date
from fintracker.models import Expense, Income
from fintracker.storage import add_expense, get_transactions, delete_transaction
from fintracker.report import generate_expenses, generate_incomings, gen_sum

"""
Модуль commands - обработчик команд для командной строки main.py.
"""
def add_command(args):
    """
    Обработчик команды add.

    Raises:
        ValueError: Ошибка ввода (указывается причина ошибки).
        Exception: Ошибка при добавлении транзакции (указывается причина ошибки).
    """
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

def view_command(args):
    """
    Обработчик команды view.

    Raises:
        ValueError: Ошибка ввода (указывается причина ошибки, чаще всего она возникает из-за неверного формата даты).
        Exception: Ошибка при просмотре транзакции (указывается причина ошибки).
    """
    start_date, end_date = None, None
    today = datetime.now()
    if args.period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1) - timedelta(microseconds=1)
    elif args.period == 'month':
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
        end_date = next_month - timedelta(microseconds=1)
    elif args.period == 'year':
        start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        next_year = start_date.replace(year=start_date.year + 1)
        end_date = next_year - timedelta(microseconds=1)
    elif args.since:
        try:
            start_date = datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            print("Ошибка формата даты для --since. Используйте YYYY-MM-DD.")
            return
    elif args.from_to:
        try:
            dates = args.from_to.split(',')
            if len(dates) == 2:
                start_date = datetime.strptime(dates[0].strip(), '%Y-%m-%d')
                end_date = datetime.strptime(dates[1].strip(), '%Y-%m-%d')
                # Устанавливаем конец дня для end_date, чтобы включить весь день
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            else:
                print("Ошибка формата для --from-to. Используйте YYYY-MM-DD,YYYY-MM-DD.")
                return
        except ValueError:
            print("Ошибка формата даты для --from-to. Используйте YYYY-MM-DD.")
            return

    try:
        df = get_transactions(start_date, end_date)
        if df.empty:
            print("Нет транзакций за указанный период.")
        else:
            print("\n Ваши Транзакции")
            print(df)
            print("-----------------------\n")
    except Exception as e:
        print(f"Произошла ошибка при просмотре транзакций: {e}")

def report_command(args):
    """
    Обработчик команды report.

    Raises:
        ValueError: Ошибка ввода (указывается причина ошибки, чаще всего она возникает из-за неверного формата даты).
    """
    start_date, end_date = None, None

    if args.period == 'month':
        today = datetime.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
        end_date = next_month - timedelta(microseconds=1)
    elif args.from_to:
        try:
            dates = args.from_to.split(',')
            if len(dates) == 2:
                start_date = datetime.strptime(dates[0].strip(), '%Y-%m-%d')
                end_date = datetime.strptime(dates[1].strip(), '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            else:
                print("Ошибка формата для --from-to. Используйте YYYY-MM-DD,YYYY-MM-DD.")
                return
        except ValueError:
            print("Ошибка формата даты для --from-to. Используйте YYYY-MM-DD.")
            return

    if args.report_type == 'categories':
        output_file = args.output if args.output else 'expenses_by_category_report.csv'
        report_df = generate_expenses(start_date, end_date, output_file)
        if not report_df.empty:
            print("\n--- Отчет по расходам по категориям ---")
            print(report_df.to_string(index=False))
            print("--------------------------------------\n")
    elif args.report_type == 'sources':
        output_file = args.output if args.output else 'incomings_by_category_report.csv'
        report_df = generate_incomings(start_date, end_date, output_file)
        if not report_df.empty:
            print("\n--- Отчет по доходам по категориям ---")
            print(report_df.to_string(index=False))
            print("--------------------------------------\n")
    elif args.report_type == 'summary':
        output_file = args.output if args.output else 'summary_report.csv'
        report_df = gen_sum(start_date, end_date, output_file)
        if not report_df.empty:
            print(report_df)
    else:
        print("Неизвестный тип отчета.")

def delete_command(args):
    """
    Обработчик команды delete.

    Raises:
        Exception: Ошибка при удалении транзакции (указывается причина ошибки, чаще всего возникает из-за того, что номера транзакции нет в базе).
    """
    if args.number is None:
        print("Ошибка: Необходимо указать номер транзакции для удаления с помощью --number.")
        return
    try:
        delete_transaction(args.number)
    except Exception as e:
        print(f"Произошла ошибка при удалении транзакции: {e}")