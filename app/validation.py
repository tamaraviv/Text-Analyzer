"""
This module provides validation functions for the input arguments of each Task.
Each function is responsible for verifying that the expected arguments are present,
no irrelevant arguments are used, and that all file paths and extensions are valid.
"""

# Import:
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


def validate_args_CountingSequences(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 2
    :param args:
    :return:
    """
    if (args.qsek_query_path is not None or args.windowsize is not None or
            args.threshold is not None or args.fixed_length is not None):
        print("invalid input")
        sys.exit(1)

    if args.maxk is None or not isinstance(args.maxk, int) or args.maxk < 0:
        print("invalid input")
        sys.exit(1)

    if args.names is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if not os.path.isfile(args.sentences) or not os.path.isfile(args.remove_words):
            print("invalid input")
            sys.exit(1)

        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if not args.sentences.endswith(".csv") or not args.remove_words.endswith(".csv"):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if not args.preprocessed.endswith(".json"):
            print("invalid input")
            sys.exit(1)
    else:
        print("invalid input")
        sys.exit(1)


def validate_args_CountingPersonMentions(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 3
    :param args:
    :return:
    """
    if (args.maxk is not None or args.qsek_query_path is not None or args.windowsize
            is not None or args.threshold is not None or args.fixed_length is not None):
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.names is not None:
        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if (not os.path.isfile(args.sentences) or not os.path.isfile(args.names)
                or not os.path.isfile(args.remove_words)):
            print("invalid input")
            sys.exit(1)

        if (not args.sentences.endswith(".csv") or not args.names.endswith(".csv") or
                not args.remove_words.endswith(".csv")):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if args.remove_words is not None:
            print("invalid input")
            sys.exit(1)

        if args.sentences is not None:
            print("invalid input")
            sys.exit(1)

        if not args.preprocessed.endswith(".json"):
            print("invalid input")
            sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)


def validate_args_SearchEngine(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 4
    :param args:
    :return:
    """
    if (args.maxk is not None or args.windowsize or args.threshold is not None
            or args.fixed_length is not None):
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is None and args.preprocessed is None:
        print("invalid input")
        sys.exit(1)

    if args.names is not None:
        print("invalid input")
        sys.exit(1)

    if not args.qsek_query_path.endswith(".json") or args.qsek_query_path is None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if not os.path.isfile(args.sentences) or not os.path.isfile(args.remove_words):
            print("invalid input")
            sys.exit(1)

        if not args.sentences.endswith(".csv") or not args.remove_words.endswith(".csv"):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if not args.preprocessed.endswith(".json"):
            print("invalid input")

            sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)


def validate_args_PersonContextAnalyzer(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 5
    :param args:
    :return:
    """
    if args.windowsize is not None or args.threshold is not None or args.fixed_length is not None:
        print("invalid input")
        sys.exit(1)

    if args.maxk is None or not isinstance(args.maxk, int) or args.maxk < 0:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if args.names is None:
            print("invalid input")
            sys.exit(1)

        if (not os.path.isfile(args.sentences) or not os.path.isfile(args.remove_words)
                or not os.path.isfile(args.names)):
            print("invalid input")
            sys.exit(1)

        if not args.sentences.endswith(".csv") or not args.remove_words.endswith(".csv"):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if not args.preprocessed.endswith(".json"):
            print("invalid input")
            sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)


def validate_args_DirectConnection(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 6
    :param args:
    :return:
    """
    if args.maxk is not None or args.qsek_query_path is not None or args.fixed_length is not None:
        print("invalid input")
        sys.exit(1)

    if args.windowsize is None or not isinstance(args.windowsize, int) or args.windowsize < 0:
        print("invalid input")
        sys.exit(1)

    if args.threshold is None or not isinstance(args.threshold, int) or args.threshold < 0:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is None and args.preprocessed is None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if (not os.path.isfile(args.sentences) or not os.path.isfile(args.names) or not os.path.isfile(
                args.remove_words)):
            print("invalid input")
            sys.exit(1)

        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if args.names is None:
            print("invalid input")
            sys.exit(1)

        if (not args.sentences.endswith(".csv") or not args.names.endswith(".csv")
                or not args.remove_words.endswith(".csv")):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if not args.preprocessed.endswith(".json"):
            print("invalid input")
            sys.exit(1)
    else:
        print("invalid input")
        sys.exit(1)


def validate_args_IndirectConnection(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 7
    :param args:
    :return:
    """
    if args.maxk is not None or args.qsek_query_path is not None or args.fixed_length is not None:
        print("invalid input")
        sys.exit(1)

    if args.maximal_distance is None or not isinstance(args.maximal_distance, int) or args.maximal_distance < 0:
        print("invalid input")
        sys.exit(1)

    if args.pairs is None:
        print("invalid input")
        sys.exit(1)

    if not args.pairs.endswith(".json"):
        print("invalid input")
        sys.exit(1)

    if not os.path.isfile(args.pairs):
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is None and args.preprocessed is None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if (not os.path.isfile(args.sentences) or not os.path.isfile(args.names)
                or not os.path.isfile(args.remove_words)):
            print("invalid input")
            sys.exit(1)

        if args.windowsize is None or not isinstance(args.windowsize, int) or args.windowsize < 0:
            print("invalid input")
            sys.exit(1)

        if args.threshold is None or not isinstance(args.threshold, int) or args.threshold < 0:
            print("invalid input")
            sys.exit(1)

        if args.names is None:
            print("invalid input")
            sys.exit(1)

        if (not args.sentences.endswith(".csv") or not args.names.endswith(".csv")
                or not args.remove_words.endswith(".csv")):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if not os.path.isfile(args.preprocessed):
            print("invalid input")
            sys.exit(1)

        if args.windowsize is not None or args.threshold is not None:
            print("invalid input")
            sys.exit(1)

        if args.sentences is not None or args.names is not None or args.remove_words is not None:
            print("invalid input")
            sys.exit(1)

        if args.preprocessed is not None:
            if not args.preprocessed.endswith(".json"):
                print("invalid input")
                sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)


def validate_args_FixedLengthPathChecker(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 8
    :param args:
    :return:
    """
    if args.maxk is not None or args.qsek_query_path is not None or args.maximal_distance is not None:
        print("invalid input")
        sys.exit(1)

    if args.fixed_length is None or not isinstance(args.fixed_length, int) or args.fixed_length < 0:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if (not os.path.isfile(args.sentences) or not os.path.isfile(args.remove_words)
                or not os.path.isfile(args.names)):
            print("invalid input")
            sys.exit(1)

    if args.pairs is None:
        print("invalid input")
        sys.exit(1)

    if not args.pairs.endswith(".json"):
        print("invalid input")
        sys.exit(1)

    if not os.path.isfile(args.pairs):
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is None and args.preprocessed is None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:

        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if args.names is None:
            print("invalid input")
            sys.exit(1)

        if args.windowsize is None or not isinstance(args.windowsize, int) or args.windowsize < 0:
            print("invalid input0")
            sys.exit(1)

        if args.threshold is None or not isinstance(args.threshold, int) or args.threshold < 0:
            print("invalid input")
            sys.exit(1)

        if (not args.sentences.endswith(".csv") or not args.names.endswith(".csv")
                or not args.remove_words.endswith(".csv")):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if args.windowsize is not None or args.threshold is not None:
            print("invalid input")
            sys.exit(1)

        if args.sentences is not None or args.names is not None or args.remove_words is not None:
            print("invalid input")
            sys.exit(1)

        if args.preprocessed is not None:
            if not os.path.isfile(args.preprocessed):
                print("invalid input")
                sys.exit(1)

            if not args.preprocessed.endswith(".json"):
                print("invalid input")
                sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)


def validate_args_SentenceClustering(args: argparse.Namespace) -> None:
    """
    this func validates arguments for task 9
    :param args:
    :return:
    """
    if (args.maxk is not None or args.qsek_query_path is not None or args.fixed_length is not None
            or args.maximal_distance is not None or args.pairs is not None or args.windowsize is not None):
        print("invalid input")
        sys.exit(1)

    if args.threshold is None or not isinstance(args.threshold, int) or args.threshold < 0:
        print("invalid input")
        sys.exit(1)

    if args.names is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None and args.preprocessed is not None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is None and args.preprocessed is None:
        print("invalid input")
        sys.exit(1)

    if args.sentences is not None:
        if not os.path.isfile(args.sentences) or not os.path.isfile(args.remove_words):
            print("invalid input")
            sys.exit(1)

        if args.remove_words is None:
            print("invalid input")
            sys.exit(1)

        if not args.sentences.endswith(".csv") or not args.remove_words.endswith(".csv"):
            print("invalid input")
            sys.exit(1)

    elif args.preprocessed is not None:
        if args.sentences is not None or args.remove_words is not None:
            print("invalid input")
            sys.exit(1)

        if args.preprocessed is not None:
            if not os.path.isfile(args.preprocessed):
                print("invalid input")
                sys.exit(1)

            if not args.preprocessed.endswith(".json"):
                print("invalid input")
                sys.exit(1)

    else:
        print("invalid input")
        sys.exit(1)
