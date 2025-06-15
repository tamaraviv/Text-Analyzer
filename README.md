# Text-Analyzer

## Overview

Text Analyzer is a modular Python project for large-scale text analysis, designed to clean,
process, and analyze textual data. It extracts recurring names, identifies direct and indirect
relationships between individuals, and detects contextual connections in raw or preprocessed
text files.
The project emphasizes clarity, modularity, and object-oriented design, making it easy to extend
and maintain.

---

## Project Structure
```
Text_analyzer/
├── app/
│   ├── __init__.py             # Module initializer
│   ├── interface.py            # CLI parser and interface logic
│   ├── logic.py                # Core task orchestration logic
│   ├── validation.py           # Validation func for each Task
│   ├── Text_Cleaner.py         # Sentence and name cleaning utilities
│   └── utils.py                # Shared utility functions
├── main.py                     # Entry point for running the program
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── test.py                     # Tests and manual validation
```
---

## 🧠 System Architecture

The system is built using **object-oriented programming**, with each major task implemented
as a self-contained class. The design allows for uniform handling of input/output while
preserving task-specific logic.

---

## 🔧 Core Components

### 🧹 Cleaning Module (`Text_Cleaner.py`)
- Removes punctuation, extra whitespace, and filtered words from input data.
  - Used across multiple tasks for consistent preprocessing.

### 🧪 Task Classes (`logic.py`)
Each task is implemented in its own class and follows a unified structure:
- `run(self)`: Determines the type of input (CSV or JSON) and triggers the appropriate process.
  - `validate_args(self, args)`: Ensures input parameters are valid (e.g., file paths, types, and
     mutually exclusive options).
  - `print_in_json(self)`: Outputs structured results in JSON format.
  - Task-specific logic is implemented inside the class, allowing for clean encapsulation.

### 🧰 Interface Module (`interface.py`)
Handles command-line argument parsing using `argparse`, including custom error handling for
invalid input.

---

## Core Capabilities

> Developed a large-scale text analysis tool featuring an algorithm capable of:
- Performing flexible and robust **text search**
  - Identifying **recurring personal names**
  - Detecting both **direct and indirect relationships** between individuals
  - Extracting **contexts** in which individuals and relations appear


## How To Run
- Use the command line to run the project by executing the main script with the appropriate
- task number and required arguments.

```bash
python main.py -t <task_number> [additional arguments]

  - | Task # | Description                        | Required Arguments                                         |
  | ------ | ---------------------------------- | ---------------------------------------------------------- |
  | 1      | Clean sentences and names          | `-s` (sentences), `-r` (remove\_words), `-n` (names)       |
  | 2      | Count k-sequences in sentences     | `-s`, `-r`, `--maxk`                                       |
  | 3      | Count mentions of each person      | `-s`, `-r`, `-n`                                           |
  | 4      | Search engine for k-sequences      | `--qsek_query_path`, `-s`, `-r`                            |
  | 5      | Analyze k-seq context per person   | `-s`, `-r`, `-n`, `--maxk`                                 |
  | 6      | Graph of direct person connections | `-s`, `-r`, `-n`, `--windowsize`, `--threshold`            |
  | 7      | Check indirect person connections  | `-s`, `-r`, `-n`, `--windowsize`, `--threshold`, `--pairs` |
  | 8      | Check fixed-length connections     | Same as Task 7 plus `--fixed_length`                       |
  | 9      | Group sentences by shared words    | `-s`, `-r`, `--threshold`                                  |
  - If any required argument is missing or incompatible with the selected task, the program will print an error message




