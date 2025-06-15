"""
Main script to run the project.

This script serves as the entry point of the application.
It initializes the user interface, executes the selected task,
and prints the results in JSON format.
"""

# Import:
from app import interface


def main():
    operator = interface.user_interface()
    operator.run()
    operator.print_in_json()


if __name__ == '__main__':
    main()
