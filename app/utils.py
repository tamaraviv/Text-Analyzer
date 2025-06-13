# Imports:
import csv
import re
import json


# function that cleans the Text

def open_csv_format_for_sentences(file_path: str) -> list[list[str]]:
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


def open_csv_format_for_name(file_path: str) -> list[list[list[str]]]:
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
                names_list = [strip_name_list(name) for name in row[0].split()]
                other_names_list = [strip_name_list(other_name) for other_name in
                                    re.split(r',', row[1].strip())]

                result.append([names_list, other_names_list])

    for sublist in result:
        if sublist[1] != ['']:
            new_other_name = [[word] for word in sublist[1]]
            sublist[1] = new_other_name
    return result


def remove_punctuations(string: str) -> str:
    """
    Remove all punctuation from a string, leaving only letters and numbers.
    """
    fixed_word = re.sub(r'[^a-zA-Z0-9 ]', ' ', str(string))
    return fixed_word


def convert_lower(string: str) -> str:
    """
    Convert a string to lowercase.
    """
    return string.lower()


def remove_whitespace(string: str) -> str:
    """
    Remove extra whitespace from a string.
    """
    return " ".join(string.split())


def remove_words(string: str, removed_words: list[str]) -> str:
    """
    Remove specific words from a string.
    """
    pattern = r'\b(' + '|'.join(re.escape(word) for word in removed_words) + r')\b'
    cleaned_string = re.sub(pattern, '', string)
    return ' '.join(cleaned_string.split())


def flatten_list(nested_list: list[list[str]]) -> list[str]:
    """
    Flatten a nested list into a single list.
    """
    return [word for sublist in nested_list for word in sublist]


def clean_string(string: str, remove_words_list: list[list[str]] | None = None) -> str:
    """
    Clean a string by removing punctuations, converting to lowercase,
    removing specific words, and removing extra whitespace.
    """
    remove_words_flat = flatten_list(remove_words_list)
    string = remove_punctuations(string)
    string = convert_lower(string)
    string = remove_words(string, remove_words_flat)
    string = remove_whitespace(string)
    return string


def remove_empty_sent(string_list: list[list[str]]) -> list[list[str]]:
    """
    Remove empty sentences from a list of lists.
    """
    return [sub_list for sub_list in string_list if sub_list and sub_list != ['']]


def turn_list_to_single_str(sentence_list: list[list[str]]) -> list[list[str]]:
    """
    Convert each sentence in a list of lists to a list of words.
    """
    return [sublist[0].split() for sublist in sentence_list]


def clean_string_no_remove_words(string: str) -> str:
    """
    Clean a string by removing punctuations, converting to lowercase,
    removing specific words, and removing extra whitespace.
    """
    string = remove_punctuations(string)
    string = convert_lower(string)
    string = remove_whitespace(string)
    return string


def remove_duplicate_words(name_list: list[list[str]]) -> list[list[str]]:
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


def replace_empty_lists_for_names(name_list: list[list[list[str]]]) -> list[list[list[str]]]:
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


def remove_empty_str_from_list(string_list: list[str]) -> list[str]:
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


def remove_empty_names(string_list: list[list[str]]) -> list[list[str]]:
    """
    this func receives a list and returns a list with no empty names
    :param string_list:
    :return:
    """
    if not string_list[0]:
        return False

    return True


def strip_name_list(string: str | None = None) -> str:
    """A placeholder clean_string function for this example."""
    if string is None:
        string = []
    if string == ['']:
        return []
    else:
        return string.strip()


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
