"""Main module of Lab_3"""
from utils.serialize import JSONSerializer


def aboba(a: int = 1, b: int = 2) -> int:
    c = 11
    return c * (a + b)


def main():
    """Carries out the subtasks of Lab_3"""
    json = JSONSerializer()
    ahuha = json.loads(json.dumps(aboba))
    print(ahuha(5, 6))


if __name__ == '__main__':
    main()
