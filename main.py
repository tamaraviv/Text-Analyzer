import csv
import re
import json
import argparse
from collections import defaultdict
import sys
from collections import deque
import os


def task1_into_lists(json_filename_path: str) -> tuple[list, list[str]]:
    """
    This function reads a JSON file and extracts the processed sentences and names.
    :param json_filename_path
    :return: A tuple containing (list of sentences, list of names)
        """
    with open(json_filename_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    sentences = data.get("Question 1", {}).get("Processed Sentences", [])
    names = data.get("Question 1", {}).get("Processed Names", [])

    return sentences, names


class CleanSentences:
    """
    this class cleans a sentences list
    """

    def __init__(self, filename_sentences: str, filename_remove_names: str | None = None):
        self.filename_sentences = filename_sentences
        self.filename_remove_names = filename_remove_names

    def open_csv_format(self, file_path: str) -> list[list[str]]:
        """
        This function receives a path to a CSV file and returns its content as a list of lists.
        """
        string = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = True
            for row in reader:
                if header:
                    header = False
                    continue
                string.append(row)
        return string

    def remove_punctuations(self, string: str) -> str:
        """
        Remove all punctuation from a string, leaving only letters and numbers.
        """
        fixed_word = re.sub(r'[^a-zA-Z0-9 ]', ' ', str(string))
        return fixed_word

    def convert_lower(self, string: str) -> str:
        """
        Convert a string to lowercase.
        """
        return string.lower()

    def remove_whitespace(self, string: str) -> str:
        """
        Remove extra whitespace from a string.
        """
        return " ".join(string.split())

    def remove_words(self, string: str, removed_words: list[str]) -> str:
        """
        Remove specific words from a string.
        """
        pattern = r'\b(' + '|'.join(re.escape(word) for word in removed_words) + r')\b'
        cleaned_string = re.sub(pattern, '', string)
        return ' '.join(cleaned_string.split())

    def flatten_list(self, nested_list: list[list[str]]) -> list[str]:
        """
        Flatten a nested list into a single list.
        """
        return [word for sublist in nested_list for word in sublist]

    def clean_string(self, string: str, remove_words_list: list[list[str]] | None = None) -> str:
        """
        Clean a string by removing punctuations, converting to lowercase,
        removing specific words, and removing extra whitespace.
        """
        remove_words_flat = self.flatten_list(remove_words_list)
        string = self.remove_punctuations(string)
        string = self.convert_lower(string)
        string = self.remove_words(string, remove_words_flat)
        string = self.remove_whitespace(string)
        return string

    def remove_empty_sent(self, string_list: list[list[str]]) -> list[list[str]]:
        """
        Remove empty sentences from a list of lists.
        """
        return [sub_list for sub_list in string_list if sub_list and sub_list != ['']]

    def turn_list_to_single_str(self, sentence_list: list[list[str]]) -> list[list[str]]:
        """
        Convert each sentence in a list of lists to a list of words.
        """
        return [sublist[0].split() for sublist in sentence_list]

    def generate_clean_sentences_list(self) -> list[list[str]]:
        """
        this func receives a path of csv format and clean the sentences file according
        to the remove names file
        :return:
        """
        sentences = self.open_csv_format(self.filename_sentences)
        remove_names = self.open_csv_format(self.filename_remove_names)

        cleaned_sentences = []
        for sentence in sentences:
            clean_sen = self.clean_string(sentence, remove_names)
            cleaned_sentences.append([clean_sen])

        cleaned_sentences = self.remove_empty_sent(cleaned_sentences)
        cleaned_sentences = self.turn_list_to_single_str(cleaned_sentences)

        return cleaned_sentences

    def clean_string_no_remove_words(self, string: str) -> str:
        """
        Clean a string by removing punctuations, converting to lowercase,
        removing specific words, and removing extra whitespace.
        """
        string = self.remove_punctuations(string)
        string = self.convert_lower(string)
        string = self.remove_whitespace(string)
        return string

    def generate_clean_sentences_list_no_remove_words(self) -> list[list[str]]:
        """
        this func generates clean sentences list without thr remove words in the given list
        :return:
        """
        sentences = self.open_csv_format(self.filename_sentences)

        cleaned_sentences = []
        for sentence in sentences:
            clean_sen = self.clean_string_no_remove_words(sentence)
            cleaned_sentences.append([clean_sen])

        cleaned_sentences = self.remove_empty_sent(cleaned_sentences)
        cleaned_sentences = self.turn_list_to_single_str(cleaned_sentences)

        return cleaned_sentences


class CleanNames:
    """
    this class creates a clean names list
    """

    def __init__(self, filename_names: str, filename_remove_names: str):
        self.filename_names = filename_names
        self.filename_remove_names = filename_remove_names

    def strip_name_list(self, string: str | None = None) -> str:
        """A placeholder clean_string function for this example."""
        if string is None:
            string = []
        if string == ['']:
            return []
        else:
            return string.strip()

    def open_csv_format_for_name(self, file_path: str) -> list[list[list[str]]]:
        """
        This func receives a path to a CSV file and returns a list of lists.
        Each inner list contains two lists: one for 'names' and one for 'other names'.
        """
        result = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = True
            for row in reader:
                if header:
                    header = False
                    continue

                if len(row) >= 2:
                    names_list = [self.strip_name_list(name) for name in row[0].split()]
                    other_names_list = [self.strip_name_list(other_name) for other_name in
                                        re.split(r',', row[1].strip())]

                    result.append([names_list, other_names_list])

        for sublist in result:
            if sublist[1] != ['']:
                new_other_name = [[word] for word in sublist[1]]
                sublist[1] = new_other_name
        return result

    def remove_duplicate_words(self, name_list: list[list[str]]) -> list[list[str]]:
        """
        this func receives a list and if there are duplicate words it returns a list that
        keeps that one that appears first
        :param name_list:
        :return: no duplicates name list
        """
        seen = set()
        unique_list = []

        for sublist in name_list:
            name = tuple(sublist[0])
            if name not in seen:
                seen.add(name)
                unique_list.append(sublist)

        return unique_list

    def replace_empty_lists_for_names(self, name_list: list[list[list[str]]]) -> list[list[list[str]]]:
        """
        This function replaces empty string (['']) in the input list with empty lists ([]).
        :param name_list: A nested list of names.
        :return: A list where empty strings are replaced with empty lists.
        """
        for sublist in name_list:
            for i in range(len(sublist)):
                if sublist[i] == ['']:
                    sublist[i] = []
        return name_list

    def remove_empty_str_from_list(self, string_list: list[str]) -> list[str]:
        """
        thus func remove any empty string from a list of strings.
        :param string_list:
        :return:
        """
        no_empty_str_list = []
        for string in string_list:
            if string != '':
                no_empty_str_list.append(string)
        return no_empty_str_list

    def remove_empty_names(self, string_list: list[list[str]]) -> list[list[str]]:
        """
        this func receives a list and returns a list with no empty names
        :param string_list:
        :return:
        """
        if string_list[0] == []:
            return False

        return True

    def generate_clean_names_list(self) -> list[list[list[str]]]:
        """
        this func receives a path of csv format and clean the names file according to the remove names file
        :return: clean_list
        """
        remove_names_format = CleanSentences(self.filename_names, self.filename_remove_names)
        names_list = self.open_csv_format_for_name(self.filename_names)
        remove_names_list = remove_names_format.open_csv_format(self.filename_remove_names)
        clean_list = []
        for sublist in names_list:
            cleaned_names = []
            cleaned_other_names = []

            for word in sublist[0]:
                new_str = remove_names_format.clean_string(word, remove_names_list)
                cleaned_names.append(new_str)

            for word in sublist[1]:
                new_str = remove_names_format.clean_string(word, remove_names_list)
                cleaned_other_names.append(new_str)

            clean_list.append([cleaned_names, cleaned_other_names])

        clean_list = self.remove_duplicate_words(clean_list)
        clean_list = self.replace_empty_lists_for_names(clean_list)

        for sublist in clean_list:
            if sublist[1] != ['']:
                new_other_name = [[word] for word in sublist[1]]
                sublist[1] = new_other_name

        for sublist in clean_list:
            sublist[1] = remove_names_format.turn_list_to_single_str(sublist[1])
        final_list = []

        for sublist in clean_list:
            if self.remove_empty_names(sublist) == True:
                final_list.append(sublist)

        for sublist in final_list:
            sublist[0] = self.remove_empty_str_from_list(sublist[0])
            sublist[1] = self.remove_empty_str_from_list(sublist[1])

        return final_list


class Task1:
    """
    this class process files into clean lists
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.filename_sentences = args.sentences
        self.filename_remove_names = args.remove_words
        self.filename_names = args.names

    def run(self):
        clean_sentence_list = CleanSentences(self.filename_sentences, self.filename_remove_names)
        clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
        self.sentence_list = clean_sentence_list.generate_clean_sentences_list()
        self.names_list = clean_names_list.generate_clean_names_list()

    def validate_args(self, args: argparse.Namespace) -> None:
        """
        this function validates arguments for task 1
        :param args:
        :return:
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


class Task2:
    """
    this class counts sequences of words in sentences
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.n = args.maxk
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def count_common_words(self, sentence_list: str, n: int) -> dict[str, list[list[str]]]:
        """
        this func receives a list of sentences and returns a dict of the count of each seq according to
        the given N
        :return: dict[str, int]
        """
        words_dict = {}
        for sublist in sentence_list:
            if len(sublist) < n:
                continue
            for i in range(len(sublist) - n + 1):
                new_word = ' '.join(sublist[i:i + n])
                if new_word in words_dict:
                    words_dict[new_word] += 1
                else:
                    words_dict[new_word] = 1

        sorted_dict = {key: words_dict[key] for key in sorted(words_dict)}

        return sorted_dict

    def put_in_format_q2(self, sentence_list: str, n: int) -> list[list[str]]:
        """
        this func receives a list of sentences and returns a dict fo the count of each seq
        :param sentence_list:
        :param n:
        :return:
        """
        words_dict = self.count_common_words(sentence_list, n)
        final_list = [f'{n}_seq']
        count_list = [[key, value] for key, value in words_dict.items()]
        final_list.append(count_list)
        return final_list

    def seq_dict(self, sentence_list: list[list[str]]) -> dict[str, int]:
        """
        this func receives a list of sentences and returns a dict with the count of each seq
        :param sentence_list:
        :return:
        """
        final_list = []
        for i in range(self.n):
            final_list.append(self.put_in_format_q2(sentence_list, i + 1))
        return final_list

    def print_in_json(self):
        """

        :return:
        """
        data = {"Question 2": {
            f'{self.n}-Seq Counts': self.seq_dict(self.sentence_list)

        }}
        print(json.dumps(data, indent=4))


class Task3:
    """
    this class counts persons name mentions in a list of sentences
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def count_names_in_sentence(self, sentence_list: list[list[str]], name_list: list[str]) -> dict[str, int]:
        """
        this func counts how many times each word occurs in the sentence and returns a dict of main name as
        key and the number of times it occurs in the sentence as value
        :param sentence_list:
        :param name_list:
        :return:
        """
        return_dict = {}
        for full_name in name_list:
            if not full_name or not full_name[0]:
                continue
            main_name = " ".join(full_name[0])
            return_dict[main_name] = 0

        for sublist in sentence_list:
            for full_name in name_list:
                main_name = " ".join(full_name[0])
                for name in full_name[0]:
                    return_dict[main_name] += sublist.count(name)

                if full_name[1]:
                    for other_name in full_name[1]:
                        return_dict[main_name] += sublist.count(other_name)

        return_dict = {key: value for key, value in return_dict.items() if value != 0}
        return_dict = {k: return_dict[k] for k in sorted(return_dict)}
        return return_dict

    def change_dict_into_list_q3(self, sentence_list: list[list[str]], name_list: list[list[str]]) -> list[list[str]]:
        """"
        this func changes dictionary into list according to the wanted format
        """
        count_name_dict = self.count_names_in_sentence(sentence_list, name_list)
        return_list = []
        for key, value in count_name_dict.items():
            return_list.append([key, value])
        return return_list

    def print_in_json(self, ):
        """
        this func runs task 3
        :return:
        """
        data = {"Question 3": {
            'Name Mentions': self.change_dict_into_list_q3(self.sentence_list, self.names_list)

        }}
        print(json.dumps(data, indent=4))


class Task4:
    """
    this class is a basic search engine functionality
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.kseq_keys = args.qsek_query_path
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def open_json_file(self):
        """
        this func opens json file
        :return:
        """
        with open(self.kseq_keys, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "keys" in data:
            return [item if isinstance(item, list) else [item] for item in data["keys"]]

        return []

    def combine_json_list(self) -> list[str]:
        """
        this func turn the json file into a list of combined strings
        :return:list[str]
        """
        new_list = []
        self.open_json_file().pop(0)
        for in_list in self.open_json_file():
            result = " ".join(in_list)
            new_list.append(result)

        return new_list

    def remove_duplicates_seq(self, kseq_keys_list: str) -> list[str]:
        """
        Removes duplicate strings from a list while maintaining order.
        :param kseq_keys_list: A list of strings.
        :return: A list with duplicates removed.
        """
        seen = set()
        cleaned_list = []
        for item in kseq_keys_list:
            if item not in seen:
                seen.add(item)
                cleaned_list.append(item)
        return cleaned_list

    def generate_all_seq_from_words_list(self, words_list: list[str], n: int | None = None) -> list[list[str]]:
        """
        this func returns a dict of all possible seq when the key is the seq and the value is all the santances
        :return:
        """
        res = []
        for start in range(len(words_list)):
            for end in range(start + 1, len(words_list) + 1):
                sub_list = words_list[start:end]
                if n is not None and len(sub_list) > n:
                    break
                res.append(sub_list)
        return res

    def generate_all_search_seq_from_sentences_list(self, sentences_list: list[str], n: int | None = None) -> dict[
        str, list[str]]:
        """
        this func returns a dict of all possible seq when the key is the seq and the value is all the santances
        :return:
        """
        seq__all_sentences_dict = defaultdict(list)
        sentences_list.sort()
        for words_list in sentences_list:
            combinations = self.generate_all_seq_from_words_list(words_list, n)
            for seq in combinations:
                seq__all_sentences_dict[' '.join(seq)].append(words_list)
        return seq__all_sentences_dict

    def count_seq_in_sentence(self, sentence_seq_dict: dict[str, list[str]], kseq_keys_list: list[str]) -> list[
        list[str]]:
        """
        this func search all seq according to the seq_list in the sentences and returns a dict when the
        key is the seq and the value is all the santances
        the O(1) - because I created a dict of all possible seq when the key is the seq and the value is all the santances
        and in this func I created a set of all the possible seq in the list so the loop if only to search
        for the correct seq matching to the key
        :return: dict[str,list[str]]
        """
        res = []
        sentence_keys_set = set(sentence_seq_dict.keys())
        for seq in sorted(kseq_keys_list):
            if seq in sentence_keys_set:
                seq_item = []
                seq_item.append(seq)
                seq_item.append(sentence_seq_dict[seq])
                res.append(seq_item)

        return res

    def print_in_json(self):
        """
        this func runs task 4
        """
        clean_search_seq_list = self.combine_json_list()
        no_dup_seq_dict = self.remove_duplicates_seq(clean_search_seq_list)
        possible_seq_dict = self.generate_all_search_seq_from_sentences_list(self.sentence_list)
        seq_dict = self.count_seq_in_sentence(possible_seq_dict, no_dup_seq_dict)
        data = {"Question 4": {
            'K-Seq Matches': seq_dict

        }}
        print(json.dumps(data, indent=4))


class Task5:
    """
    this class returns the contexts of people and associated K-seqs
    """

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.validate_args(args)
        self.n = args.maxk
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.args.names = None
        self.args.maxk = None
        self.args.qsek_query_path = "ignore.json"
        self.task4 = Task4(self.args)

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()


        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def check_names_in_sentences(self, sentence_list: list[list[str]], names_list: list[list[str]]) -> dict[
        str, list[str]]:
        """
        this func checks names in sentences and returns a dict of names as keys and lists of santances as values
        :return: dict[main_name,list[sentence]]
        """
        return_dict = {}
        sorted_sentences_list = sorted(sentence_list, key=lambda x: x[0])
        for full_name in names_list:
            main_name = " ".join(full_name[0])
            return_dict[main_name] = []

        for sublist in sorted_sentences_list:
            for full_name in names_list:
                main_name = " ".join(full_name[0])
                for name in full_name[0]:
                    if name in sublist:
                        return_dict[main_name].append(sublist)

                for other_name in full_name[1]:
                    if other_name in sublist:
                        return_dict[main_name].append(sublist)

        for key in return_dict:
            return_dict[key] = [list(sublist) for sublist in {tuple(sublist) for sublist in return_dict[key]}]

        for key in return_dict:
            return_dict[key] = sorted(return_dict[key])

        return_dict = {key: value for key, value in return_dict.items() if value != []}
        return_dict = {k: return_dict[k] for k in sorted(return_dict.keys())}

        return return_dict

    def get_sentences_with_search_names(self, names_santances_dict: dict[str, list[str]]) -> list[list[str]]:
        """
        this func returns a list of lists when the first item, is the name and all possible
         seq of the associated santances as values
        :return: list[list[str]]
        """
        res = []
        for key, value in names_santances_dict.items():
            item = [key]
            seq_name_dict = self.task4.generate_all_search_seq_from_sentences_list(value, self.n)
            seq_list = []
            for name in seq_name_dict.keys():
                name = name.split(' ')
                seq_list.append(name)

            seq_list.sort()
            item.append(seq_list)
            res.append(item)

        return res

    def print_in_json(self):
        """
        this func runs task 5
        :return:
        """
        dict_of_seq = self.check_names_in_sentences(self.sentence_list, self.names_list)
        res_dict = self.get_sentences_with_search_names(dict_of_seq)
        if self.n == 0:
            data = {"Question 5": {
                'Person Contexts and K-Seqs': []
            }}
        else:
            data = {"Question 5": {
                'Person Contexts and K-Seqs': res_dict
            }}

        print(json.dumps(data, indent=4))


class Task6:
    def __init__(self, args: argparse.Namespace) -> None:
        self.validate_args(args)
        self.k = args.windowsize
        self.t = args.threshold
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def all_possible_pairs_list(self, names_list: list[list[str]]) -> list[list[str]]:
        """
        this func creates all possible pairs
        """
        pairs = []
        for i in range(len(names_list)):
            for j in range(i + 1, len(names_list)):
                pairs.append([names_list[i], names_list[j]])

        return pairs

    def check_names_in_sentence(self, sentences_list: list[list[str]], k: int) -> dict[tuple[str, str], int]:
        """
        this func checks if there is a mention of a pair of names in a window - k of sentences
        :return:
        """
        count_mention_dict = {}
        pairs_list = self.all_possible_pairs_list(self.names_list)

        if k > len(sentences_list):
            print('invalid input')
            sys.exit(1)

        for i in range(len(sentences_list) - k + 1):
            window_sentences = sentences_list[i:i + k]

            for pair in pairs_list:
                name1, name2 = pair[0], pair[1]

                name1_found = False
                name2_found = False

                for sentence in window_sentences:
                    for full_name_1 in name1:
                        for main_name_1 in full_name_1:
                            if main_name_1 in sentence:
                                name1_found = True

                    for full_name_2 in name2:
                        for main_name_2 in full_name_2:
                            if main_name_2 in sentence:
                                name2_found = True

                if name1_found and name2_found:
                    name1_string = ' '.join(name1[0])
                    name2_string = ' '.join(name2[0])
                    pair_key = (name1_string, name2_string)
                    count_mention_dict[pair_key] = count_mention_dict.get(pair_key, 0) + 1

        return count_mention_dict

    def check_move_edges(self, dict_pairs: dict[str, int], t: int) -> list[list[list[str]]]:
        """
        this func returns all the edges that are larger than t
        :param dict_pairs:
        :param t:
        :return:
        """
        edges = []
        for names, count in dict_pairs.items():
            if count >= t:
                names_list = [name.split() for name in names]
                edges.append(names_list)

        return edges

    def sort_pairs_list(self, pairs_dict: dict[str, int]) -> dict[str, list[str]]:
        """
        this func sort a list of pairs
        :return:
        """
        sorted_data = [sorted(pair, key=lambda x: ' '.join(x)) for pair in pairs_dict]
        sorted_data.sort(key=lambda pair: (' '.join(pair[0]), ' '.join(pair[1])))

        return sorted_data

    def print_in_json(self):
        """
        this func runs task 6
        :return:
        """
        count_pairs_in_w_dict = self.check_names_in_sentence(self.sentence_list, self.k)
        pairs_list = self.check_move_edges(count_pairs_in_w_dict, self.t)
        data = {"Question 6": {
            'Pair Matches': self.sort_pairs_list(pairs_list)
        }}

        print(json.dumps(data, indent=4))


class Task7:
    """
    this class determent indirect connections through a graph
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.max_dist = args.maximal_distance
        self.connection_names_list = args.pairs
        self.args = args
        del self.args.maximal_distance
        del self.args.pairs
        if self.filename_sentences:
            self.k = args.windowsize
            self.t = args.threshold

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()
            self.graph = Task6(self.args)
            self.graph.run()


        elif self.filename_preprocessed:
            self.sentence_list = self.filename_preprocessed
            self.graph = None

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def open_json_into_list_task6(self) -> list[list[str]]:
        """
        this func opens a json file from task 6 and reads it into a list
        """
        with open(self.sentence_list, 'r') as file:
            data = json.load(file)

        if "Question 6" not in data:
            print('invalid input')
            sys.exit(1)

        if "Pair Matches" not in data["Question 6"]:
            print('invalid input')
            sys.exit(1)

        pair_matches = []

        for pair in data["Question 6"]["Pair Matches"]:
            pair_matches.append([pair[0], pair[1]])
        return pair_matches

    def open_json_into_list_people_connection(self) -> list[list[str]]:
        """
        this func opens a json file in the people_connection format and reads it into a list
        """
        with open(self.connection_names_list, 'r') as file:
            data = json.load(file)

        return data["keys"]

    def build_graph(self) -> dict[str, list]:
        """
        this func builds a graph according to the pairs in the people_connections_filename
        :return: dict[str, list]
        """
        neighbors_graph: defaultdict[str, set[str]] = defaultdict(set)

        if self.graph:
            count_mentions: dict[tuple[str, str], int] = self.graph.check_names_in_sentence(self.sentence_list, self.k)
            for (name1, name2), count in count_mentions.items():
                if count >= self.t:
                    neighbors_graph[name1].add(name2)
                    neighbors_graph[name2].add(name1)
        else:
            pairs = self.open_json_into_list_task6() if (
                    "Pair Matches" in self.connection_names_list) else self.open_json_into_list_people_connection()
            for pair in pairs:
                name1, name2 = pair[0], pair[1]
                neighbors_graph[name1].add(name2)
                neighbors_graph[name2].add(name1)

        return neighbors_graph

    def check_remote_connection_pairs(self, name1, name2) -> bool:
        """
        this func checks if two names has a remote connection until max distance is reached
        :param name1:
        :param name2:
        :return:bool
        """
        if self.graph:
            new_graph = self.build_graph()

        else:
            pairs = self.open_json_into_list_task6()
            flattened_lists = []
            for pair in pairs:
                flattened_pairs = [[' '.join(sublist)] for sublist in pair]
                flattened_lists.append(flattened_pairs)

            new_graph = {}

            for pair in flattened_lists:
                pair1, pair2 = pair[0][0], pair[1][0]

                if pair1 not in new_graph:
                    new_graph[pair1] = []
                if pair2 not in new_graph:
                    new_graph[pair2] = []

                new_graph[pair1].append(pair2)
                new_graph[pair2].append(pair1)

        if name1 not in new_graph or name2 not in new_graph:
            return False

        if new_graph == {}:
            return False

        inital_name = deque([(name1, 0)])
        visited = set()

        while inital_name:
            current, distance = inital_name.popleft()

            if current == name2:
                return True

            if distance < self.max_dist:
                for neighbor in new_graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        inital_name.append((neighbor, distance + 1))

        return False

    def print_in_json(self):
        """
        this func runs task 7
        :return:
        """
        res = []

        if self.graph:
            for name1, name2 in self.open_json_into_list_people_connection():
                res.append([name1, name2, self.check_remote_connection_pairs(name1, name2)])
        else:
            for name1, name2 in self.open_json_into_list_people_connection():
                res.append([name1, name2, self.check_remote_connection_pairs(name1, name2)])

        for item in res:
            item[:2] = sorted(item[:2])
        sorted_res = sorted(res, key=lambda x: (x[0], x[1]))

        data = {"Question 7": sorted_res,
                }

        print(json.dumps(data, indent=4))


class Task8:
    """
    this class checks fixed-length paths between people
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.fixed_length = args.fixed_length
        self.connection_names_list = args.pairs
        self.args = args
        args.fixed_length = None
        del self.args.pairs
        if self.filename_sentences:
            self.k = args.windowsize
            self.t = args.threshold

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()
            self.graph = Task6(self.args)
            self.graph.run()

        elif self.filename_preprocessed:
            self.sentence_list = self.filename_preprocessed
            self.graph = None

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def open_json_into_list_task6(self) -> list[list[str]]:
        """
        this func opens a json file from, task 6 and reads it into a list
        """
        with open(self.sentence_list, 'r') as file:
            data = json.load(file)

        if "Question 6" not in data:
            print('invalid input')

        if "Pair Matches" not in data["Question 6"]:
            print('invalid input')

        pair_matches = []

        for pair in data["Question 6"]["Pair Matches"]:
            pair_matches.append([pair[0], pair[1]])
        return pair_matches

    def open_json_into_list(self) -> list[list[str]]:
        """
        Opens a json file from the people_connections format and reads it into a list
        """
        with open(self.connection_names_list, 'r') as file:
            data = json.load(file)

        return data["keys"]

    def build_graph(self) -> dict[str, list[str]]:
        """
        Builds a graph according to the pairs in the people_connections_filename.
        :return: dict[str, list]
        """
        neighbors_graph: defaultdict[str, set[str]] = defaultdict(set)
        count_mentions: dict[tuple[str, str], int] = self.graph.check_names_in_sentence(self.sentence_list, self.k)
        for (name1, name2), count in count_mentions.items():
            if count >= self.t:
                neighbors_graph[name1].add(name2)
                neighbors_graph[name2].add(name1)

        return neighbors_graph

    def check_fixed_path_connection(self, name1: str, name2: str) -> bool:
        """
        This function checks if two names are connected by a fixed-length path (no loops allowed).
        :param name1: First name
        :param name2: Second name
        :return: True if they are connected by a path of length self.path_length, otherwise False.
        """
        if self.graph:
            new_graph = self.build_graph()

        else:
            pairs = self.open_json_into_list_task6()
            flattened_lists = []
            for pair in pairs:
                flattened_pairs = [[' '.join(sublist)] for sublist in pair]
                flattened_lists.append(flattened_pairs)

            new_graph = {}

            for pair in flattened_lists:
                pair1, pair2 = pair[0][0], pair[1][0]

                if pair1 not in new_graph:
                    new_graph[pair1] = []
                if pair2 not in new_graph:
                    new_graph[pair2] = []

                new_graph[pair1].append(pair2)
                new_graph[pair2].append(pair1)

        if name1 not in new_graph or name2 not in new_graph:
            return False

        inital_name = deque([(name1, [name1])])
        visited = set()

        while inital_name:
            current, path = inital_name.popleft()

            if current == name2 and len(path) == self.fixed_length:
                return True

            if current not in visited:
                visited.add(current)

                for neighbor in new_graph[current]:
                    if neighbor not in path:
                        inital_name.append((neighbor, path + [neighbor]))

        return False

    def print_in_json(self):
        """
        This function runs task 8 and prints the results in JSON format.
        :return:
        """
        res = []
        for name1, name2 in self.open_json_into_list():
            res.append([name1, name2, self.check_fixed_path_connection(name1, name2)])

        for item in res:
            item[:2] = sorted(item[:2])
        sorted_res = sorted(res, key=lambda x: (x[0], x[1]))

        data = {"Question 8": sorted_res, }

        print(json.dumps(data, indent=4))


class Task9:
    """
    this class is grouping sentences by shared words
    """

    def __init__(self, args: argparse.Namespace):
        self.validate_args(args)
        self.t = args.threshold
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]

        self.graph = self.build_graph()

    def validate_args(self, args: argparse.Namespace) -> None:
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

    def build_graph(self) -> dict[int, list[int]]:
        """
        this func builds a graph, if two sentences have more then t number of common words then
        the index number of ine of them is added as key and the index number of the second is
        added as value.
        :return:dict[int:list[int]]
        """
        graph: dict[int, list[int]] = {}
        for i in range(len(self.sentence_list)):
            for j in range(i + 1, len(self.sentence_list)):
                common_words = set(self.sentence_list[i]) & set(self.sentence_list[j])

                if len(common_words) >= self.t:
                    if i not in graph:
                        graph[i] = []
                    if j not in graph:
                        graph[j] = []

                    graph[i].append(j)
                    graph[j].append(i)

        return graph

    def find_groups(self) -> list[list[str]]:
        """
        Finds and returns all groups of connected sentences in the graph.
        """
        visited = set()
        groups: list[list[str]] = []

        def dfs(node: str, group: list[str]) -> None:
            """Performs Depth-First Search to find all connected components."""
            visited.add(node)
            group.append(node)
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, group)

        for node in range(len(self.sentence_list)):
            if node not in visited:
                group: list[str] = []
                dfs(node, group)
                in_list = []
                for index in group:
                    in_list.append(self.sentence_list[int(index)])
                groups.append(in_list)

        return groups

    def sort_groups(self, groups_list: list[list[str]]) -> list[list[str]]:
        """
        this func sorts the groups of connected sentences in the graph and returns a dict of the number
        of group as key and all sorted sentences as values.
        :return:
        """
        for sublist in groups_list:
            sublist.sort()

        return sorted(groups_list, key=lambda x: (len(x), x))

    def print_in_json(self):
        """
        this func runs task 9
        :return:
        """
        return_list = []
        groups_list = self.find_groups()
        sorted_groups_list = self.sort_groups(groups_list)
        for i, group in enumerate(sorted_groups_list, 1):
            return_list.append([f'Group {i}', group])

        data = {"Question 9": {
            "group Matches": return_list,

        }}

        print(json.dumps(data, indent=4))


def main():
    """
    this func runs the final project
    :return:
    """

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
        task = Task1(args)

    if args.task == 2:
        task = Task2(args)

    if args.task == 3:
        task = Task3(args)

    if args.task == 4:
        task = Task4(args)

    if args.task == 5:
        task = Task5(args)

    if args.task == 6:
        task = Task6(args)

    if args.task == 7:
        task = Task7(args)

    if args.task == 8:
        task = Task8(args)

    if args.task == 9:
        task = Task9(args)

    task.run()
    task.print_in_json()


if __name__ == '__main__':
    main()
