"""Main module of Lab_3"""
from utils.serialize import JSONSerializer


def aboba(a: int = 1, b: int = 2) -> int:
    c = 11
    return c * (a + b)


def main():
    """Carries out the subtasks of Lab_3"""
    json = JSONSerializer()
    ahuha = json.loads(json.dumps(aboba))
    print(dir(ahuha.__code__) == dir(aboba.__code__))
    print(aboba.__code__.co_code == ahuha.__code__.co_code)
    print(aboba.__code__.co_code)
    print(ahuha.__code__.co_code)

    # print(json._process_dict(json._parse_dictlike(json.dumps(aboba))))


if __name__ == '__main__':
    main()
