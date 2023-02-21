import enum


@enum.unique
class Command(enum.Enum):
    add = "add"
    remove = "remove"
    find = "find"
    list = "list"
    grep = "grep"
    save = "save"
    load = "load"
    switch = "switch"
