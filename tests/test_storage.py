import pandas as pd
from fintracker.models import Expense, Income
from datetime import datetime
import unittest

"""
Модуль storage - добавление, удаление транзакций.
"""

DATA_FILE = 'C:/Users/user/fintr/transactions.csv'

def _load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из CSV таблицы и преобразует их в DataFrame.
    Returns:
        df: Датафрейм с транзакциями.
    Raises:
        Exceprion: Если произошла ошибка при чтении файла.
    """
    try:
        df = pd.read_csv(DATA_FILE, encoding='cp1251', sep=';')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        print(f"Ошибка при чтении файла {DATA_FILE}: {e}")
        return pd.DataFrame(columns=['type', 'description', 'amount', 'category', 'source', 'date'])

def _save_transactions(df: pd.DataFrame):
    """
    Сохраняет транзакции в файл

       Args:
           df(pd.DataFrame): Датафрейм с транзакциями

       Raises:
            Exceprion: Если произошла ошибка при чтении файла.
    """
    try:
        df.to_csv(DATA_FILE, sep=';', index=False, encoding='cp1251')
        print(f"Данные успешно сохранены в {DATA_FILE}")
    except Exception as e:
        print(f"Ошибка при сохранении файла {DATA_FILE}: {e}")
def add_expense(transaction):
    """
    Подготавливает данные для записи в файл

    Returns:
        new_row: подготовленный датафрейм для записи в таблицу.
    """
    df = _load_transactions()
    if isinstance(transaction, Expense):
        new_row = pd.DataFrame([{
            'type': 'Расход',
            'description': transaction.description,
            'amount': transaction.amount,
            'category': transaction.category,
            'source': None,
            'date': transaction.date
        }])
    elif isinstance(transaction, Income):
        new_row = pd.DataFrame([{
            'type': 'Доход',
            'description': transaction.description,
            'amount': transaction.amount,
            'category': None,
            'source': transaction.source,
            'date': transaction.date
        }])
    else:
        print("Неподдерживаемый тип транзакции.")
        return

    df = pd.concat([df, new_row], ignore_index=True)
    _save_transactions(df)

def get_transactions(start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
    """Фильтрует датафрейм по заданным условиям
    Args:
        start_date(datetime): начальная дата фильтррации
        end_date(datetime): конечная дата фильтрации

    Returns:
        df: отфильтрованный датафрейм
    """
    df = _load_transactions()
    if not start_date and not end_date:
        return df
    if start_date:
        df = df[df['date'] >= start_date]
    if end_date:
        df = df[df['date'] <= end_date]

    return df

def delete_transaction(transaction_id: int):
    """
    Удаляет транзакцию под заданным номером

    Args:
        transaction_id(int): номер транзакции, который требуется удалить
    """
    df = _load_transactions()
    if 0 <= transaction_id < len(df):
        df = df.drop(transaction_id).reset_index(drop=True)
        _save_transactions(df)
        print(f"Транзакция под номером {transaction_id} удалена.")
    else:
        print(f"Ошибка: Транзакция под номером {transaction_id} не найдена.")

class TestModels(unittest.TestCase):
    def test_e(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        e = Expense('test', 45, 'test', date)
        self.assertEqual(repr(e), '<Expense: test, 45.00, Category: test, Date: 2026-01-09>')

    def test_i(self):
        e = "<Income: test, 45.00, Source: test, Date: 2026-01-09>"
        date = datetime(2026, 1, 9, 12, 00, 00)
        f = Income('test', 45, 'test', date)
        self.assertEqual(repr(f), e)

    def test_ed(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        e = Expense('test', 45, 'test', date)
        self.assertEqual(e.description, 'test')

    def test_ea(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        e = Expense('test', 45, 'test', date)
        self.assertEqual(e.amount, 45)

    def test_edate(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        e = Expense('test', 45, 'test', date)
        self.assertEqual(e.date, date)

    def test_id(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        i = Income('test', 45, 'test', date)
        self.assertEqual(i.description, 'test')

    def test_ia(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        i = Income('test', 45, 'test', date)
        self.assertEqual(i.amount, 45)

    def test_idate(self):
        date = datetime(2026, 1, 9, 12, 00, 00)
        i = Income('test', 45, 'test', date)
        self.assertEqual(i.date, date)
