"""
Main script to run the project.
"""

# Import:
import interface


def main():
    operator = interface.user_interface()
    operator.run()
    operator.print_in_json()


if __name__ == '__main__':
    main()
