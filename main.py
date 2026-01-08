import argparse
from fintracker import commands

def main():
    parser = argparse.ArgumentParser(description="CLI Финансовый трекер расходов и доходов.")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Команда добавления транзакции --add
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

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
