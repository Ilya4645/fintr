import pandas as pd
from datetime import datetime, date
from fintracker.storage import get_transactions
"""
Модуль report - генерирует отчеты по заданным условиям.
"""
def generate_expenses(start_date: datetime = None, end_date: datetime = None, output_file: str = None) -> pd.DataFrame:
    """
    Генерирует отчет по расходам по заданным условиям и сохраняет его в файл.

    Args:
        start_date(datetime): начальная дата фильтрации.
        end_date(datetime): конечная дата фильтрации.
        output_file(str): название файла для сохранения отчета (по умолчанию - expenses_by_category_report.csv).

    Returns:
        report - датафрейм с отчетом.
    """
    df = get_transactions(start_date, end_date)
    exp_df = df[df['type'] == 'Расход']

    if exp_df.empty:
        print("Нет данных о расходах для формирования отчета.")
        return pd.DataFrame()

    report = exp_df.groupby('category')['amount'].sum().reset_index()
    report.rename(columns={'amount': 'total_amount'}, inplace=True)
    report = report.sort_values(by='total_amount', ascending=False)

    if output_file:
        try:
            report.to_csv(output_file, index=False, encoding='cp1251', sep=';')
            print(f"Отчет о расходах по категориям сохранен в {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении отчета в файл {output_file}: {e}")

    return report

def generate_incomings(start_date: datetime = None, end_date: datetime = None, output_file: str = None) -> pd.DataFrame:
    """
    Генерирует отчет по доходам по заданным условиям и сохраняет его в файл.

    Args:
        start_date(datetime): начальная дата фильтрации.
        end_date(datetime): конечная дата фильтрации.
        output_file(str): название файла для сохранения отчета (по умолчанию - incomings_by_category_report.csv).

    Returns:
        report - датафрейм с отчетом.
    """
    df = get_transactions(start_date, end_date)
    inc_df = df[df['type'] == 'Доход']

    if inc_df.empty:
        print("Нет данных о доходах для формирования отчета.")
        return pd.DataFrame()

    report = inc_df.groupby('source')['amount'].sum().reset_index()
    report.rename(columns={'amount': 'total_amount'}, inplace=True)
    report = report.sort_values(by='total_amount', ascending=False)

    if output_file:
        try:
            report.to_csv(output_file, index=False, encoding='cp1251', sep=';')
            print(f"Отчет о доходах по категориям сохранен в {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении отчета в файл {output_file}: {e}")

    return report

def gen_sum(start_date: datetime = None, end_date: datetime = None, output_file: str = None):
    """
    Генерирует общий отчет по заданным условиям и сохраняет его в файл.

    Args:
        start_date(datetime): начальная дата фильтрации.
        end_date(datetime): конечная дата фильтрации.
        output_file(str): название файла для сохранения отчета (по умолчанию - summary_report.csv).

    Returns:
        report - датафрейм с отчетом.
        """
    df = get_transactions(start_date, end_date)
    if df.empty:
        print("Нет данных для формирования сводного отчета.")
        return
    sum_in = df[df['type'] == 'Доход']['amount'].sum()
    sum_ex = df[df['type'] == 'Расход']['amount'].sum()
    balance = sum_in - sum_ex

    report = pd.DataFrame({
        'Сводный отчет': '',
        'Период c': [start_date.strftime('%Y-%m-%d') if start_date else date.today()],
        'Период по': [end_date.strftime('%Y-%m-%d') if end_date else date.today()],
        'Общий доход': sum_in,
        'Общий расход': sum_ex,
        'Баланс': balance}).transpose()

    if output_file:
        try:
            report.to_csv(output_file, encoding='cp1251', sep=';')
            print(f"Отчет о доходах по категориям сохранен в {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении отчета в файл {output_file}: {e}")

    return report




