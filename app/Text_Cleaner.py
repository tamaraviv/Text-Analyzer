"""
This module defines the core data classes used for text cleaning and preprocessing.

Classes:
    - CleanSentences: Handles loading and preprocessing of sentence data.
    - CleanNames: Handles loading and cleaning of name data, including filtering unwanted names.
"""

# Import project files:
from . import utils


class CleanSentences:
    """
       A class responsible for cleaning and preprocessing a list of sentences,
       such as removing punctuation, converting to lowercase, and removing unwanted words.

       Attributes:
           filename_sentences (str): Path to the input CSV file containing sentences.
           filename_remove_names (str | None): Path to the file containing words to remove.
       """

    def __init__(self, filename_sentences: str, filename_remove_names: str | None = None):
        self.filename_sentences = filename_sentences
        self.filename_remove_names = filename_remove_names


    def generate_clean_sentences_list(self) -> list[list[str]]:
        """
        Generates a cleaned list of tokenized sentences, using a list of words to remove.

        Returns:
            list[list[str]]: A list of sentences, each represented as a list of words.
        """
        sentences = utils.open_csv_format_for_sentences(self.filename_sentences)
        remove_names = utils.open_csv_format_for_sentences(self.filename_remove_names)

        cleaned_sentences = []
        for sentence in sentences:
            clean_sen = utils.clean_string(sentence, remove_names)
            cleaned_sentences.append([clean_sen])

        cleaned_sentences = utils.remove_empty_sent(cleaned_sentences)
        cleaned_sentences = utils.turn_list_to_single_str(cleaned_sentences)

        return cleaned_sentences

    def generate_clean_sentences_list_no_remove_words(self) -> list[list[str]]:
        """
        this func generates clean sentences list without the remove words in the given list
        :return:
        """
        sentences = utils.open_csv_format_for_sentences(self.filename_sentences)

        cleaned_sentences = []
        for sentence in sentences:
            clean_sen = utils.clean_string_no_remove_words(sentence)
            cleaned_sentences.append([clean_sen])

        cleaned_sentences = utils.remove_empty_sent(cleaned_sentences)
        cleaned_sentences = utils.turn_list_to_single_str(cleaned_sentences)

        return cleaned_sentences


class CleanNames:
    """
    A class responsible for cleaning and structuring a list of names, including
    primary and alternative names, while filtering out undesired entries.

    Attributes:
        filename_names (str): Path to the CSV file with names.
        filename_remove_names (str): Path to the CSV file with names to be removed.
    """

    def __init__(self, filename_names: str, filename_remove_names: str):
        self.filename_names = filename_names
        self.filename_remove_names = filename_remove_names


    def generate_clean_names_list(self) -> list[list[list[str]]]:
        """
        Cleans and structures the names file into nested lists of valid names.

        Returns:
            list[list[list[str]]]: A cleaned list of names, where each element is a pair of lists:
                                   [cleaned_main_names, cleaned_other_names]
        """
        names_list = utils.open_csv_format_for_name(self.filename_names)
        remove_names_list = utils.open_csv_format_for_sentences(self.filename_remove_names)
        clean_list = []
        for sublist in names_list:
            cleaned_names = []
            cleaned_other_names = []

            for word in sublist[0]:
                new_str = utils.clean_string(word, remove_names_list)
                cleaned_names.append(new_str)

            for word in sublist[1]:
                new_str = utils.clean_string(word, remove_names_list)
                cleaned_other_names.append(new_str)

            clean_list.append([cleaned_names, cleaned_other_names])

        clean_list = utils.remove_duplicate_words(clean_list)
        clean_list = utils.replace_empty_lists_for_names(clean_list)

        for sublist in clean_list:
            if sublist[1] != ['']:
                new_other_name = [[word] for word in sublist[1]]
                sublist[1] = new_other_name

        for sublist in clean_list:
            sublist[1] = utils.turn_list_to_single_str(sublist[1])
        final_list = []

        for sublist in clean_list:
            if utils.remove_empty_names(sublist):
                final_list.append(sublist)

        for sublist in final_list:
            sublist[0] = utils.remove_empty_str_from_list(sublist[0])
            sublist[1] = utils.remove_empty_str_from_list(sublist[1])

        return final_list
