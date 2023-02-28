"""Types for Task_2"""
import enum


@enum.unique
class Command(enum.Enum):
    """Represents commands available in CLI"""
    add = "add"
    remove = "remove"
    find = "find"
    list = "list"
    grep = "grep"
    save = "save"
    load = "load"
    switch = "switch"
