import argparse
from fintracker import commands
"""
Главный модуль. Использует argparse для обработки аргументов.
"""
def main():
    """Добавление команд."""
    parser = argparse.ArgumentParser(description="CLI Финансовый трекер расходов и доходов.")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    """Команда добавления транзакции --add"""
    parser_add = subparsers.add_parser('add', help='Добавить новую транзакцию (расход или доход)')
    parser_add.add_argument('--description', required=True, help='Описание транзакции')
    parser_add.add_argument('--sum', type=float, required=True, help='Сумма транзакции')
    parser_add.add_argument('--date', help='Дата транзакции в формате YYYY-MM-DD. По умолчанию - текущая дата.')

    add_group = parser_add.add_mutually_exclusive_group(required=True)
    add_group.add_argument('--expense', action='store_true', help='Указывает, что это расход.')
    add_group.add_argument('--income', action='store_true', help='Указывает, что это доход.')

    parser_add.add_argument('--category', help='Категория расхода (обязательно для --expense)')
    parser_add.add_argument('--source', help='Источник дохода (обязательно для --income)')
    parser_add.set_defaults(func=commands.add_command)

    """Команда просмотра транзакций --view"""
    parser_view = subparsers.add_parser('view', help='Просмотреть транзакции')
    parser_view.add_argument('--period', choices=['day', 'month', 'year'], help='Период просмотра (день, месяц, год)')
    parser_view.add_argument('--since', help='Просмотреть транзакции с указанной даты (YYYY-MM-DD)')
    parser_view.add_argument('--from-to', help='Просмотреть транзакции в диапазоне дат (YYYY-MM-DD,YYYY-MM-DD)')
    parser_view.set_defaults(func=commands.view_command)

    """Команда генерации отчетов --report"""
    parser_report = subparsers.add_parser('report', help='Сгенерировать отчет')
    parser_report.add_argument('--report-type', choices=['categories', 'summary', 'sources'], required=True, help='Тип отчета: "categories" (расходы по категориям), "sources" (доходы) или "summary" (сводный отчет).')
    parser_report.add_argument('--period', choices=['month'], help='Период для отчета "categories".')
    parser_report.add_argument('--from-to', help='Диапазон дат для отчета (YYYY-MM-DD,YYYY-MM-DD).')
    parser_report.add_argument('--output', help='Имя файла для сохранения отчета (CSV). Если не указано, будет использовано имя по умолчанию.')
    parser_report.set_defaults(func=commands.report_command)

    """Команда удаления транзакции --delete"""
    parser_delete = subparsers.add_parser('delete', help='Удалить транзакцию по номеру')
    parser_delete.add_argument('--number', type=int, required=True, help='Номер транзакции для удаления (см. вывод команды view)')
    parser_delete.set_defaults(func=commands.delete_command)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
