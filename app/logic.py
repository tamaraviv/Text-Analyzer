"""

This module implements the core algorithms used throughout the project.

"""

# Import python library:
import json
import argparse
import sys
import os

import Text_Cleaner


class CleanText:
    """
    A class that processes input CSV files and produces cleaned lists of sentences and names.
    """

    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        self.names_list = None
        self.validate_args(args)
        self.filename_sentences = args.sentences
        self.filename_remove_names = args.remove_words
        self.filename_names = args.names

    def run(self):
        clean_sentence_list = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
        clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
        self.sentence_list = clean_sentence_list.generate_clean_sentences_list()
        self.names_list = clean_names_list.generate_clean_names_list()

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def print_in_json(self):
        """
        this func prints clean sentences list and clean names list into a json file
        :return:
        """
        data = {"Question 1": {
            "Processed Sentences": self.sentence_list,
            "Processed Names": self.names_list
        }}

        print(json.dumps(data, indent=4))
