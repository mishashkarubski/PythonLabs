"""Main module of Lab_1/Task_1"""
import helpers


def main():
    """Carries out the subtasks of Task_1"""

    print("Hello, World!")  # Subtask 1 – printing "Hello, World!".

    try:  # Subtask 2 – math operations.
        x, y = map(float, input(
            "Enter two numbers separated by space: ").split())
        print("1. Result of addition is",
              f"{helpers.calculate(x, y, 'add')}")
        print("2. Result of multiplication",
              f"is {helpers.calculate(x, y, 'mult')}")
        print("3. Result of substration is",
              f"{helpers.calculate(x, y, 'sub')}")
        print("4. Result of division is",
              f"{helpers.calculate(x, y, 'div')}")
    except ValueError:
        print("Found invalid numbers. Skipping.")

    # Subtask 3 – filtering even numbers from the given input.
    numbers = list(input("Enter numbers separated by space: ").split())
    print("5. Even numbers of the list of integers from your input are:",
          f"{' '.join(helpers.filter_even(numbers))}")


if __name__ == "__main__":
    main()
