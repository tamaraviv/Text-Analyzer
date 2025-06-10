# Text-Analyzer

## Text Analysis & Relationship Detection Tool

This project is a large-scale text analysis system designed to process, clean, and analyze
textual data for discovering recurring names, identifying relationships between individuals, and
extracting contextual connections. It was built using Python and follows an object-oriented
architecture.

---

## Project Structure & Design

The system is designed with clarity and modularity in mind, using **object-oriented programming.
Each task is encapsulated in a dedicated class with a consistent internal structure, allowing
for reusable, maintainable, and scalable code.

## Core Classes

- **Data Cleaning Classes**
  These classes receive CSV files, remove unnecessary spaces, punctuation, and filtered words
  based on a given list. They are used frequently across tasks and are therefore separated from
  Task 1 for convenience and modular reuse.

- **Task Classes**
  Each task is implemented in its own class, which includes the following structure:

  - `run(self)`: Initializes the task based on the given arguments. Automatically distinguishes
     between:
    - Preprocessed JSON input
    - Raw CSV input that needs to be cleaned

  - `validate_args(self, args)`: Validates all input parameters, ensuring correct file paths,
   types, and mutual exclusivity of options.

  - **Task-specific logic**: Varies per task and includes analysis or search functionality.

  - `print_in_json(self)`: Exports the results in a clear, structured JSON format for readability
   and further use.


## Unified Execution

A main function handles the execution of the program, allowing each task to run in a uniform way
while still preserving the logic specific to each task.

---

## Core Capabilities

> Developed a large-scale text analysis tool featuring an algorithm capable of:
- Performing flexible and robust **text search**
- Identifying **recurring personal names**
- Detecting both **direct and indirect relationships** between individuals
- Extracting **contexts** in which individuals and relations appear


## How To Run
- .klj;lj;
