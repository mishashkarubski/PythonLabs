"""Main module of Lab_1/Task_1"""
import helpers


def main():
    """Carries out the subtasks of Task_1"""

    print("Hello, World!")
    print("1. Result of addition is",
          f"{helpers.mathfunc(4, -11, 'add')}")
    print("2. Result of multiplication",
          f"is {helpers.mathfunc(4., -1.1, 'mult')}")
    print("3. Result of substration is",
          f"{helpers.mathfunc(4.2, -11, 'sub')}")
    print("4. Result of division is",
          f"{helpers.mathfunc(-4.2, 0, 'div')}")
    print("5. Even numbers of list of integers from 0 to 50 are:",
          f"{helpers.filter_even(list(range(51)))}")


if __name__ == "__main__":
    main()
