"""
This module implements the core algorithms used throughout the project.

It contains the main logic for each task, including:
- Text processing and sequence generation
- Search and graph operations
- Name recognition and context analysis

Each Task class (Task1 to Task9) imports and uses functions from this module as needed.
"""

# Import python library:
import json
import argparse
import sys
from collections import defaultdict, deque

# Import project files:
from . import Text_Cleaner
from . import utils
from . import validation


class CleanText:
    """
    A class that processes input CSV files and produces cleaned lists of sentences and names.
    """

    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        self.names_list = None
        validation.validate_args_CleanText(args)
        self.filename_sentences = args.sentences
        self.filename_remove_names = args.remove_words
        self.filename_names = args.names

    def run(self):
        clean_sentence_list = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
        clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
        self.sentence_list = clean_sentence_list.generate_clean_sentences_list()
        self.names_list = clean_names_list.generate_clean_names_list()

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


class CountingSequences:
    """
    This class counts common sequences of consecutive words (k-seqs) in a list of sentences.

    For a given maximum sequence length N, it generates dictionaries for all values of k where
     1 <= k <= N.
    Each dictionary maps a string representing a k-length sequence of words to the number of times
    that sequence appears across all sentences.

    Note:
        Each sentence is processed independently, without considering surrounding sentences.
    """

    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        validation.validate_args_CountingSequences(args)
        self.n = args.maxk
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]


    def seq_dict(self, sentence_list: list[list[str]]) -> dict[str, int]:
        """
        this func receives a list of sentences and returns a dict with the count of each seq
        :param sentence_list:
        :return:
        """
        final_list = []
        for i in range(self.n):
            final_list.append(utils.put_in_format_task2(sentence_list, i + 1))
        return final_list

    def print_in_json(self):
        """

        :return:
        """
        data = {"Question 2": {
            f'{self.n}-Seq Counts': self.seq_dict(self.sentence_list)

        }}
        print(json.dumps(data, indent=4))


class CountingPersonMentions:
    """
    This class counts how many times each person's name appears in a given text,
    including any alternate names or nicknames.

    For each person listed in the People file, the counter considers both the main name
    and all names listed under the "Other Names" column. Each occurrence of these
    names in the text is counted toward the total for that person.

    Use Case:
        Useful for tracking references to individuals in large texts, accounting for variations
        in how each person may be mentioned.

    """

    def __init__(self, args: argparse.Namespace):
        self.names_list = None
        self.sentence_list = None
        validation.validate_args_CountingPersonMentions(args)
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def print_in_json(self, ):
        """
        this func runs task 3
        :return:
        """
        data = {"Question 3": {
            'Name Mentions': utils.change_dict_into_list_q3(self.sentence_list, self.names_list)

        }}
        print(json.dumps(data, indent=4))


class SearchEngine:
    """
    This class implements a basic search engine for k-sequences (k-seqs) of words.

    Given:
        - A JSON file containing a list of k-seqs (each k-seq is a list of consecutive words).
        - A CSV file containing sentences.

    The engine builds a data structure that maps each k-seq to the list of cleaned sentences
    in which it appears. Once constructed, each search for a k-seq is performed in O(1) time.

    Use Case:
        Efficiently find all sentences that contain specific k-word sequences.

    Notes:
        - The construction of the internal index may take more than O(1), but each individual
          lookup is guaranteed to be constant time.
        - The choice of data structure (e.g., dictionary-based inverted index) is crucial to
          achieving this performance.

    """

    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        validation.validate_args_SearchEngine(args)
        self.kseq_keys = args.qsek_query_path
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]

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

    def print_in_json(self):
        """
        this func runs task 4
        """
        clean_search_seq_list = self.combine_json_list()
        no_dup_seq_dict = utils.remove_duplicates_seq(clean_search_seq_list)
        possible_seq_dict = utils.generate_all_search_seq_from_sentences_list(self.sentence_list)
        seq_dict = utils.count_seq_in_sentence(possible_seq_dict, no_dup_seq_dict)
        data = {"Question 4": {
            'K-Seq Matches': seq_dict

        }}
        print(json.dumps(data, indent=4))


class PersonContextAnalyzer:
    """
    This class analyzes the textual context in which each person is mentioned by extracting
     k-sequences (k-seqs) from sentences that mention them.

    Given:
        - An integer N specifying the maximum k-seq length.
        - A People file mapping main names to their alternate names.
        - A list of sentences.

    For each person, the class identifies all sentences in which they are mentioned (either by their main name
    or any of their alternate names), and extracts all k-seqs (for 1 <= k <= N) that appear in those sentences.

    Output:
        A lexicographically sorted dictionary where:
        - Keys are person names.
        - Values are lists of k-seqs (as strings) that appeared in the same sentence as the person.

    Use Case:
        Useful for understanding the context in which individuals are discussed in text, such as in articles,
        reports, or conversations.

    """


    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        self.names_list = None
        self.args = args
        validation.validate_args_PersonContextAnalyzer(args)
        self.n = args.maxk
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.args.names = None
        self.args.maxk = None
        self.args.qsek_query_path = "ignore.json"

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()


        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def get_sentences_with_search_names(self, names_santances_dict: dict[str, list[str]]) -> list[list[str]]:
        """
        this func returns a list of lists when the first item, is the name and all possible
         seq of the associated santances as values
        :return: list[list[str]]
        """
        res = []
        for key, value in names_santances_dict.items():
            item = [key]
            seq_name_dict = utils.generate_all_search_seq_from_sentences_list(value, self.n)
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
        dict_of_seq = utils.check_names_in_sentences(self.sentence_list, self.names_list)
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



class PeopleDirectConnectionGraph:
    """
    This class constructs a BFS graph representing direct connections between people based on
    their proximity within a text.

    Two people are considered connected if they are mentioned within the same sliding window
    of consecutive sentences. An edge is created between two people if they co-occur in at least
    't' such windows, where 't' is a given threshold.

    Graph Structure:
        - Nodes: Represent individuals from the People file.
        - Edges: Represent strong connections (based on threshold t) between individuals who
                 frequently appear together within sentence windows of size k.

    Input:
        - A list of sentences.
        - A People file (main names and alternate names).
        - Window size (number of consecutive sentences).
        - Threshold t for minimum co-occurrence.

    Output:
        A list of edges (pairs of person names) representing the resulting graph.

    Use Case:
        Useful for analyzing social or narrative connections, such as in articles, books, or
        transcripts.

    """

    def __init__(self, args: argparse.Namespace) -> None:
        self.sentence_list = None
        self.names_list = None
        validation.validate_args_DirectConnection(args)
        self.k = args.windowsize
        self.t = args.threshold
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]
            self.names_list = clean_sentence_and_names[1]

    def check_names_in_sentence(self, sentences_list: list[list[str]], k: int) -> dict[tuple[str, str], int]:
        """
        this func checks if there is a mention of a pair of names in a window - k of sentences
        :return:
        """
        count_mention_dict = {}
        pairs_list = utils.all_possible_pairs_list(self.names_list)

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


    def print_in_json(self):
        """
        this func runs task 6
        :return:
        """
        count_pairs_in_w_dict = self.check_names_in_sentence(self.sentence_list, self.k)
        pairs_list = utils.check_move_edges(count_pairs_in_w_dict, self.t)
        data = {"Question 6": {
            'Pair Matches': utils.sort_pairs_list(pairs_list)
        }}

        print(json.dumps(data, indent=4))



class IndirectConnection:
    """
    This class checks for indirect connections between people in a graph representing their
     co-occurrences.

    Given:
        - A graph G where nodes are people and edges represent direct connections (from PeopleDirectConnectionGraph).
        - A list of person-pairs (Name1, Name2) from the main "Name" column of the People file.

    The class determines whether each pair of people is connected by any path in the graph,
    including indirect connections through intermediate individuals ("friends of friends").

    Output:
        A list of lists, where each sublist contains:
            [Name1, Name2, True/False]
        indicating whether there is a path between Name1 and Name2 in the graph.

    Use Case:
        Helps uncover hidden or indirect relationships between individuals in a textual dataset.

    """

    def __init__(self, args: argparse.Namespace):
        self.names_list = None
        self.graph = None
        self.sentence_list = None
        validation.validate_args_IndirectConnection(args)
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
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()
            self.graph = PeopleDirectConnectionGraph(self.args)
            self.graph.run()


        elif self.filename_preprocessed:
            self.sentence_list = self.filename_preprocessed

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


class FixedLengthPathChecker:
    """
    This class extends graph analysis by checking whether two people are connected
    through a path of **exactly** a specified length in an undirected graph,
    without revisiting any node (i.e., no cycles or repeated nodes are allowed).

    Given:
        - A graph G (from Task 6) with people as nodes.
        - A list of person-pairs (Name1, Name2).
        - A fixed path length L.

    For each pair, the class determines whether there exists a simple path (no repeated nodes)
    of exactly length L connecting the two people.

    Output:
        A list of lists, where each sublist contains:
            [Name1, Name2, L, True/False]
        indicating whether a simple path of length L exists between the two people.

    Use Case:
        Useful for identifying specific levels of relationship, such as:
        - Are two people connected through exactly 2 intermediaries?
        - Detecting structured or layered connections in a network.

    Attributes:
        graph (dict): Adjacency list representation of the undirected graph G.
    """


    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        self.names_list = None
        validation.validate_args_FixedLengthPathChecker(args)
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.fixed_length = args.fixed_length
        self.connection_names_list = args.pairs
        self.args = args
        args.fixed_length = None
        self.graph = None
        del self.args.pairs
        if self.filename_sentences:
            self.k = args.windowsize
            self.t = args.threshold

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()
            clean_names_list = Text_Cleaner.CleanNames(self.filename_names, self.filename_remove_names)
            self.names_list = clean_names_list.generate_clean_names_list()
            self.graph = PeopleDirectConnectionGraph(self.args)
            self.graph.run()

        elif self.filename_preprocessed:
            self.sentence_list = self.filename_preprocessed

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


class SentenceClustering:
    """
    This class groups sentences based on shared word content using a graph-based approach.

    Each sentence is treated as a node in an undirected graph. An edge is added between two sentences
    if they share at least T distinct words (T is a configurable threshold).

    Once the graph is constructed, connected components are identified. Each connected component
    represents a group of related sentences. A sentence with no connections forms a group of its own.

    Requirements:
        - Word matching is based on distinct words (repeated words do not increase the match count).
        - Words do not need to be consecutive in the sentence.
        - Matching is case-insensitive and may exclude punctuation (depending on preprocessing).

    Input:
        - A list of cleaned sentences.
        - An integer threshold T specifying the minimum number of shared words for a connection.

    Output:
        - A list of sentence groups, where each group is a list of sentence indices or texts
          that are mutually connected.

    Use Case:
        Useful for clustering related sentences in documents, chat transcripts, or articles
        based on topical similarity or common vocabulary.

    """

    def __init__(self, args: argparse.Namespace):
        self.sentence_list = None
        validation.validate_args_SentenceClustering(args)
        self.t = args.threshold
        self.filename_remove_names = args.remove_words
        self.filename_sentences = args.sentences
        self.filename_names = args.names
        self.filename_preprocessed = args.preprocessed
        self.graph = None

    def run(self):
        if self.filename_sentences:
            all_sentences = Text_Cleaner.CleanSentences(self.filename_sentences, self.filename_remove_names)
            self.sentence_list = all_sentences.generate_clean_sentences_list()

        elif self.filename_preprocessed:
            clean_sentence_and_names = utils.task1_into_lists(self.filename_preprocessed)
            self.sentence_list = clean_sentence_and_names[0]

        self.graph = self.build_graph()

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

        def dfs(node_g: str, group_g: list[str]) -> None:
            """Performs Depth-First Search to find all connected components."""
            visited.add(node_g)
            group_g.append(node_g)
            for neighbor in self.graph.get(node_g, []):
                if neighbor not in visited:
                    dfs(neighbor, group_g)

        for node in range(len(self.sentence_list)):
            if node not in visited:
                group: list[str] = []
                dfs(node, group)
                in_list = []
                for index in group:
                    in_list.append(self.sentence_list[int(index)])
                groups.append(in_list)

        return groups


    def print_in_json(self):
        """
        this func runs task 9
        :return:
        """
        return_list = []
        groups_list = self.find_groups()
        sorted_groups_list = utils.sort_groups(groups_list)
        for i, group in enumerate(sorted_groups_list, 1):
            return_list.append([f'Group {i}', group])

        data = {"Question 9": {
            "group Matches": return_list,

        }}

        print(json.dumps(data, indent=4))
