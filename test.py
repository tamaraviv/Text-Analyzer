import main
import unittest
from unittest.mock import mock_open
from unittest.mock import patch
import tempfile
import csv
import json
import os
import argparse
import pytest


class TestTask1IntoLists(unittest.TestCase):

    def setUp(self):
        self.temp_json_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')

        json_data = {
            "Question 1": {
                "Processed Sentences": [
                    ["John", "met", "Alice"],
                    ["Alice", "and", "Bob", "are", "friends"],
                    ["Bob", "knows", "Charlie"]
                ],
                "Processed Names": ["John", "Alice", "Bob", "Charlie"]
            }
        }

        json.dump(json_data, self.temp_json_file, indent=4)
        self.temp_json_file.close()

    def tearDown(self):
        os.remove(self.temp_json_file.name)

    def test_task1_into_lists(self):
        sentences, names = main.task1_into_lists(self.temp_json_file.name)
        expected_sentences = [
            ["John", "met", "Alice"],
            ["Alice", "and", "Bob", "are", "friends"],
            ["Bob", "knows", "Charlie"]
        ]
        expected_names = ["John", "Alice", "Bob", "Charlie"]

        self.assertEqual(sentences, expected_sentences)
        self.assertEqual(names, expected_names)


class TestGenerateCleanNamesList(unittest.TestCase):
    def setUp(self):
        self.temp_names_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        writer = csv.writer(self.temp_names_file)
        writer.writerow(["Name", "Other Name"])
        writer.writerow(["David", "Cohen"])
        writer.writerow(["Alice", ""])
        writer.writerow(["", "Bob"])
        self.temp_names_file.close()

        self.temp_remove_names_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        writer = csv.writer(self.temp_remove_names_file)
        writer.writerow(["Remove Name"])
        writer.writerow(["Alice"])
        self.temp_remove_names_file.close()

        self.instance = main.CleanNames(self.temp_names_file.name, self.temp_remove_names_file.name)

    def test_generate_clean_names_list(self):
        result = self.instance.generate_clean_names_list()

        expected_result = [[['david'], [['cohen']]], [['alice'], []]]
        self.assertEqual(result, expected_result)

    def tearDown(self):
        import os
        os.remove(self.temp_names_file.name)
        os.remove(self.temp_remove_names_file.name)


class TestCleanStringNoRemoveWords(unittest.TestCase):

    def setUp(self):
        self.cleaner = main.CleanSentences('temp.csv', 'temp2.csv')

    def test_clean_string_no_remove_words(self):
        input_string = "Hello World"
        expected_output = "hello world"
        self.assertEqual(self.cleaner.clean_string_no_remove_words(input_string), expected_output)

        input_string = "Hello, World!"
        expected_output = "hello world"
        self.assertEqual(self.cleaner.clean_string_no_remove_words(input_string), expected_output)

        input_string = "   Hello     World   "
        expected_output = "hello world"
        self.assertEqual(self.cleaner.clean_string_no_remove_words(input_string), expected_output)

        input_string = "  Hello,    World!   "
        expected_output = "hello world"
        self.assertEqual(self.cleaner.clean_string_no_remove_words(input_string), expected_output)

        input_string = "HeLLo WoRLd"
        expected_output = "hello world"
        self.assertEqual(self.cleaner.clean_string_no_remove_words(input_string), expected_output)


class TestOpenCsvFormat_sentence(unittest.TestCase):

    def setUp(self):
        self.temp_csv_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(self.temp_csv_file)

        csv_writer.writerow(["Name", "Age", "City"])
        csv_writer.writerow(["Alice", "25", "New York"])
        csv_writer.writerow(["Bob", "30", "Los Angeles"])
        csv_writer.writerow(["Charlie", "35", "Chicago"])

        self.temp_csv_file.close()

        self.task = main.CleanSentences("dummy.csv", 'dummy_remove.csv')

    def tearDown(self):
        os.remove(self.temp_csv_file.name)

    def test_open_csv_format_sentences(self):
        result = self.task.open_csv_format(self.temp_csv_file.name)
        expected_result = [
            ["Alice", "25", "New York"],
            ["Bob", "30", "Los Angeles"],
            ["Charlie", "35", "Chicago"]
        ]

        self.assertEqual(result, expected_result)


class TestOpenCsvFormat_names(unittest.TestCase):

    def setUp(self):
        self.temp_csv_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(self.temp_csv_file)

        csv_writer.writerow(["Name", "other_name"])
        csv_writer.writerow(["Alice", "New York"])
        csv_writer.writerow(["Bob", "Los Angeles"])
        csv_writer.writerow(["Charlie", "Chicago"])

        self.temp_csv_file.close()

        self.task = main.CleanNames("dummy.csv", 'dummy_remove.csv')

    def tearDown(self):
        os.remove(self.temp_csv_file.name)

    def test_open_csv_format_sentences(self):
        result = self.task.open_csv_format_for_name(self.temp_csv_file.name)
        expected_result = [[['Alice'], [['New York']]],
                           [['Bob'], [['Los Angeles']]],
                           [['Charlie'], [['Chicago']]]]

        self.assertEqual(result, expected_result)


class TestCleanSentences(unittest.TestCase):

    def test_remove_punctuations(self):
        """
        test if the func remove punctuations correctly
        """
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        result_1 = clean_sentences.remove_punctuations("Hello, world!")
        result_2 = clean_sentences.remove_punctuations("")
        result_3 = clean_sentences.remove_punctuations("@#%jo went.. to the")
        result_4 = clean_sentences.remove_punctuations("%$^&*($@")
        result_5 = clean_sentences.remove_punctuations("Joe1 He$Llo YO#U8 are Ve..Ry NI,,ce")
        self.assertEqual(result_1, "Hello  world ")
        self.assertEqual(result_2, "")
        self.assertEqual(result_3, "   jo went   to the")
        self.assertEqual(result_4, "        ")
        self.assertEqual(result_5, "Joe1 He Llo YO U8 are Ve  Ry NI  ce")

    def test_flatten_list(self):
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        nested_list = [["John", "met"], [], ["Alice", "and", "Bob"]]
        flattened = clean_sentences.flatten_list(nested_list)
        self.assertEqual(flattened, ["John", "met", "Alice", "and", "Bob"])

    def test_convert_lower(self):
        """
        test if the func does lower the string correctly
        """
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        result_1 = clean_sentences.convert_lower("HELLO WORLD")
        result_2 = clean_sentences.convert_lower('Joe1 HeLlo YOU8 are VeRy NIce')
        result_3 = clean_sentences.convert_lower('')
        result_4 = clean_sentences.convert_lower("Y")
        result_5 = clean_sentences.convert_lower("%^&H")

        self.assertEqual(result_1, "hello world")
        self.assertEqual(result_2, 'joe1 hello you8 are very nice')
        self.assertEqual(result_3, "")
        self.assertEqual(result_4, "y")
        self.assertEqual(result_5, "%^&h")

    def test_remove_whitespace(self):
        """
        test if the func removes whitespace correctly
        :return:
        """
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        result_1 = clean_sentences.remove_whitespace("   Hello     world   ")
        result_2 = clean_sentences.remove_whitespace("")
        result_3 = clean_sentences.remove_whitespace("%&* hou  poiu  ")
        result_4 = clean_sentences.remove_whitespace("            ")
        result_5 = clean_sentences.remove_whitespace(" T ")

        self.assertEqual(result_1, "Hello world")
        self.assertEqual(result_2, "")
        self.assertEqual(result_3, "%&* hou poiu")
        self.assertEqual(result_4, "")
        self.assertEqual(result_5, "T")

    def test_remove_words(self):
        """
        test if the func removes words from a string correctly
        :return:
        """
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        result_1 = clean_sentences.remove_words("Hello world", ["world"])
        result_2 = clean_sentences.remove_words('hi how are you today', [])
        result_3 = clean_sentences.remove_words('', ["world"])
        result_4 = clean_sentences.remove_words('I thought you didnt wanted to come so', ['you', 'are', 'so'])
        result_5 = clean_sentences.remove_words('you love $', ['hi'])
        self.assertEqual(result_1, "Hello")
        self.assertEqual(result_2, 'hi how are you today')
        self.assertEqual(result_3, '')
        self.assertEqual(result_4, 'I thought didnt wanted to come')
        self.assertEqual(result_5, 'you love $')

    def test_remove_empty_sent(self):
        """
        test if the func returns a list of lists without emtpy lists inside
        :return:
        """
        clean_sentences = main.CleanSentences("sentences.csv", "remove_names.csv")
        result_1 = clean_sentences.remove_empty_sent([['Hello world'], [], []])
        result_2 = clean_sentences.remove_empty_sent([['Hello world'], [''], ['']])
        result_3 = clean_sentences.remove_empty_sent([[], [], []])
        result_4 = clean_sentences.remove_empty_sent([])
        result_5 = clean_sentences.remove_empty_sent([['k'], [], []])
        self.assertEqual(result_1, [['Hello world']])
        self.assertEqual(result_2, [['Hello world']])
        self.assertEqual(result_3, [])
        self.assertEqual(result_4, [])
        self.assertEqual(result_5, [['k']])


class TestGenerateCleanSentencesListNoRemoveWords(unittest.TestCase):

    def setUp(self):
        self.temp_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        writer = csv.writer(self.temp_csv)

        writer.writerow(["sentence"])
        writer.writerow(["Hello, world!"])
        writer.writerow(["   This   is   a   test.   "])
        writer.writerow(["Python, is great!"])
        writer.writerow([""])

        self.temp_csv.close()

        self.cleaner = main.CleanSentences(self.temp_csv.name)

    def tearDown(self):
        os.remove(self.temp_csv.name)

    def test_generate_clean_sentences_list_no_remove_words(self):
        expected_output = [['hello', 'world'],
                           ['this', 'is', 'a', 'test'],
                           ['python', 'is', 'great']]

        result = self.cleaner.generate_clean_sentences_list_no_remove_words()
        self.assertEqual(result, expected_output)


class TestRemoveEmptyNames(unittest.TestCase):

    def setUp(self):
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')

        data = {
            "names": [[[''], ['']], [["David"], ['cohen']]]
        }

        json.dump(data, self.temp_json)
        self.temp_json.close()

        with open(self.temp_json.name, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)

        self.input_data = loaded_data["names"]
        self.cleaner = main.CleanNames('name.csv', 'remove_name.csv')

    def tearDown(self):
        os.remove(self.temp_json.name)

    def test_remove_empty_names(self):
        expected_output = True

        result = self.cleaner.remove_empty_names(self.input_data)
        self.assertEqual(result, expected_output)


class TestGenerateCleanSentencesList(unittest.TestCase):
    """

    """

    def setUp(self):
        self.temp_sentences_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.temp_sentences_file.write(
            'John met Alice\nAlice and Bob are friends\nBob knows Charlie\nCharlie loves Alice\n')
        self.temp_sentences_file.close()

        self.temp_remove_names_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.temp_remove_names_file.write('Alice\nBob\n')
        self.temp_remove_names_file.close()

        self.task = main.CleanSentences(self.temp_sentences_file.name, self.temp_remove_names_file.name)

    def tearDown(self):
        os.remove(self.temp_sentences_file.name)
        os.remove(self.temp_remove_names_file.name)

    def test_generate_clean_sentences_list(self):
        cleaned_sentences = self.task.generate_clean_sentences_list()

        expected_result = [['alice', 'and', 'bob', 'are', 'friends'],
                           ['bob', 'knows', 'charlie'],
                           ['charlie', 'loves', 'alice']]
        self.assertEqual(cleaned_sentences, expected_result)


class TestCleanNames(unittest.TestCase):

    def test_remove_duplicate_words(self):
        """
        test if the func removes duplicate words from a string correctly
        :return:
        """
        clean_names = main.CleanNames("sentences.csv", "remove_names.csv")

        input_data = [
            [["John"], ["Doe"]],
            [["Jane"], ["Smith"]],
            [["John"], ["Doe"]],
            [["Alice"], [""]],
            [["Jane"], ["Smith"]],
            [["Bob"], ["Builder"]],
            [["Alice"], [""]],
        ]
        expected_output = [
            [["John"], ["Doe"]],
            [["Jane"], ["Smith"]],
            [["Alice"], [""]],
            [["Bob"], ["Builder"]],
        ]
        self.assertEqual(clean_names.remove_duplicate_words(input_data), expected_output)

        input_data = []
        expected_output = []
        self.assertEqual(clean_names.remove_duplicate_words(input_data), expected_output)

        input_data = [
            [[""], [""]],
            [[""], [""]],
        ]
        expected_output = [
            [[""], [""]],
        ]
        self.assertEqual(clean_names.remove_duplicate_words(input_data), expected_output)

        input_data = [
            [["John"], ["Doe"]],
            [["Doe"], ["John"]],
        ]
        expected_output = [
            [["John"], ["Doe"]],
            [["Doe"], ["John"]],
        ]
        self.assertEqual(clean_names.remove_duplicate_words(input_data), expected_output)

    def test_replace_empty_lists_for_names(self):
        """
        test if the func replace empty lists in thr names lists
        :return:
        """
        clean_names = main.CleanNames('sentences.csv"', "remove_names.csv")
        input_data = [
            [['John'], ['']],
            [['Jane'], ['Smith']],
            [[''], ['']],
            [['Alice'], ['Bob']],
        ]
        expected_output = [
            [['John'], []],
            [['Jane'], ['Smith']],
            [[], []],
            [['Alice'], ['Bob']],
        ]
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

        input_data = []
        expected_output = []
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

        input_data = [
            [[], []],
            [[], []],
        ]
        expected_output = [
            [[], []],
            [[], []],
        ]
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

        input_data = [
            [['John'], ['Doe']],
            [['Jane'], ['Smith']],
        ]
        expected_output = [
            [['John'], ['Doe']],
            [['Jane'], ['Smith']],
        ]
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

        input_data = [[[''], []]]
        expected_output = [[[], []]]
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

        input_data = []
        expected_output = []
        self.assertEqual(clean_names.replace_empty_lists_for_names(input_data), expected_output)

    def test_remove_duplicates_words(self):
        """this test if the func remove duplicate words"""
        clean_names = main.CleanNames("sentences.csv", "remove_names.csv")

        input_data_1 = [[['John', 'Doe'], []], [['Jane', 'Smith'], []], [['John', 'Doe'], []]]
        expected_output_1 = [[['John', 'Doe'], []], [['Jane', 'Smith'], []]]
        self.assertEqual(clean_names.remove_duplicate_words(input_data_1), expected_output_1)

        input_data_2 = []
        expected_output_2 = []
        self.assertEqual(clean_names.remove_duplicate_words(input_data_2), expected_output_2)

        input_data_3 = [[['John'], []], [['Jane', 'Smith'], []], [['huo'], ['john']]]
        expected_output_3 = [[['John'], []], [['Jane', 'Smith'], []], [['huo'], ['john']]]
        self.assertEqual(clean_names.remove_duplicate_words(input_data_3), expected_output_3)

        input_data_4 = [[['John', 'Doe'], []], [['Jane', 'Doe'], []], [['John', 'Doe'], []]]
        expected_output_4 = [[['John', 'Doe'], []], [['Jane', 'Doe'], []]]
        self.assertEqual(clean_names.remove_duplicate_words(input_data_4), expected_output_4)

        input_data_5 = [[['Alice', 'Wonderland'], []], [['Bob', 'Builder'], []], [['Alice', 'Wonderland'], []]]
        expected_output_5 = [[['Alice', 'Wonderland'], []], [['Bob', 'Builder'], []]]
        self.assertEqual(clean_names.remove_duplicate_words(input_data_5), expected_output_5)

        input_data_6 = [[['John', 'Smith'], []], [['Smith', 'John'], []], [['John', 'Smith'], []]]
        expected_output_6 = [[['John', 'Smith'], []], [['Smith', 'John'], []]]
        self.assertEqual(clean_names.remove_duplicate_words(input_data_6), expected_output_6)


if __name__ == '__main__':
    unittest.main()
