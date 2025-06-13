"""
This module initializes and runs the user interface.
"""

# Import from python library:
import argparse
import sys

# import project files:
import logic
from add_to_git.Text_analyzer.logic import CleanText


def user_interface():
    """
     this func runs the final project
     :return:
     """

    task = None

    class CustomParser(argparse.ArgumentParser):
        def error(self, message):
            print("invalid input")
            sys.exit(1)

    parser = CustomParser()
    parser.add_argument('-t', '--task', type=int, help="task number", required=True)
    parser.add_argument('--maxk', type=int, help="seq number")
    parser.add_argument('-s', '--sentences', type=str, help="sentence_list")
    parser.add_argument('-n', '--names', type=str, help="people_list")
    parser.add_argument('-r', '--remove_words', type=str, help="remove_names_filename")
    parser.add_argument('--preprocessed', type=str, help="processed_json_file")
    parser.add_argument('--qsek_query_path', type=str, help="kseq_filename")
    parser.add_argument('--windowsize', type=int, help="windowsize")
    parser.add_argument('--threshold', type=int, help="threshold")
    parser.add_argument('--pairs', type=str, help="pairs file")
    parser.add_argument('--maximal_distance', type=int, help="maximal_distance")
    parser.add_argument('--fixed_length', type=int, help="fixed_length")
    args = parser.parse_args()

    if args.task not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("invalid input")
        sys.exit(1)

    if args.task == 1:
        task = logic.CleanText(args)

    return task

