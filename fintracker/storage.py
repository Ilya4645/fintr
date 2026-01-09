import pandas as pd
from fintracker.models import Expense, Income
from datetime import datetime
import sqlite3

"""
Модуль storage - добавление, удаление транзакций.
"""

DATA_FILE = 'C:/Users/user/fintr/fintr.db'
BACKUP_FILE = 'C:/Users/user/fintr/transactions_backup.csv'

def _load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из базы данных и преобразует их в DataFrame.
    Returns:
        df: Датафрейм с транзакциями.
    Raises:
        Exceprion: Если произошла ошибка при чтении БД.
    """
    try:
        conn = sqlite3.connect(DATA_FILE)
        query = 'SELECT * From transactions ORDER BY date ASC'
        df = pd.read_sql(query, conn)
        df['date'] = pd.to_datetime(df['date'])
        conn.close()
        return df
    except Exception as e:
        print(f"Ошибка при чтении БД: {e}")
        return pd.DataFrame(columns=['type', 'description', 'amount', 'category', 'source', 'date'])

def _save_transactions(df: pd.DataFrame):
    """
    Сохраняет транзакции в БД

       Args:
           df(pd.DataFrame): Датафрейм с транзакциями

       Raises:
            Exceprion: Если произошла ошибка при чтении файла.
    """
    try:
        conn = sqlite3.connect(DATA_FILE)
        df.to_sql('transactions', conn, if_exists='append', index=False)
        print(f"Данные успешно записаны в базу данных")
        conn.close()
    except Exception as e:
        print(f"Ошибка при записи данных в БД: {e}")
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

    _save_transactions(new_row)

def save_backup():
    """
    Сохраняет транзакции из Датафрейма (предварительно, сформировав его из БД) в CSV файл.

    Raises:
        Exceprion: Если произошла ошибка при сохранении.
    """
    try:
        df = _load_transactions()
        df.to_csv(BACKUP_FILE, index=False, encoding='cp1251', sep=';')
        print(f"Копия транзакций сохранена в файле {BACKUP_FILE}")
    except Exception as e:
        print(f"Ошибка при сохранении копии в файл {BACKUP_FILE}: {e}")

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
