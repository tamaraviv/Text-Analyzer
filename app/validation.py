"""
This module
"""
import argparse
import sys
import os


def validate_args_CleanText(args: argparse.Namespace) -> None:
    """
    Validates the input arguments for Task 1.

    :param args: Parsed command-line arguments
    :return: None; exits the program on invalid input
    """

    if (args.maxk is not None or args.qsek_query_path is not None or args.preprocessed is not None
            or args.windowsize is not None or args.threshold is not None or args.fixed_length is not None):
        print("invalid input")
        sys.exit(1)

    if args.sentences is None or args.remove_words is None or args.names is None:
        print("invalid input")
        sys.exit(1)

    if not os.path.isfile(args.sentences) or not os.path.isfile(args.names) or not os.path.isfile(
            args.remove_words):
        print("invalid input")
        sys.exit(1)

    if (not args.sentences.endswith(".csv") or not args.names.endswith(".csv") or
            not args.remove_words.endswith(".csv")):
        print("invalid input")
        sys.exit(1)

