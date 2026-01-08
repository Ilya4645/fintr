import pandas as pd
from fintracker.models import Expense, Income
from datetime import datetime

DATA_FILE = 'transactions.csv'

def _load_transactions() -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['type', 'description', 'amount', 'category', 'source', 'date'])
    except Exception as e:
        print(f"Ошибка при чтении файла {DATA_FILE}: {e}")
        return pd.DataFrame(columns=['type', 'description', 'amount', 'category', 'source', 'date'])

def _save_transactions(df: pd.DataFrame):
    try:
        df.to_csv(DATA_FILE, sep=';', mode='a', index=False, header=False, encoding='cp1251')
        print(f"Данные успешно сохранены в {DATA_FILE}")
    except Exception as e:
        print(f"Ошибка при сохранении файла {DATA_FILE}: {e}")
def add_expense(transaction):
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
