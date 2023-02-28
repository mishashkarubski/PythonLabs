"""Main module of Lab_2/Task_2"""
from typing import NoReturn

from utils.entities.console import Console


def main() -> NoReturn:
    """Carries out the subtasks of Task_2"""
    cli: Console = Console()
    cli.start_session()

if __name__ == '__main__':
    main()
    