# Cognifyz Technologies - Software Development Internship 🚀

[![Live Website](https://img.shields.io/badge/Live%20Demo-Website%20Active-brightgreen.svg?style=for-the-badge&logo=google-chrome)](https://ksomesha13-cpu.github.io/Cognifyz-Software-Development-Internship/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue.svg?style=for-the-badge&logo=github)](https://github.com/ksomesha13-cpu/Cognifyz-Software-Development-Internship)

🌐 **Live Interactive Website:** **[https://ksomesha13-cpu.github.io/Cognifyz-Software-Development-Internship/](https://ksomesha13-cpu.github.io/Cognifyz-Software-Development-Internship/)**

![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/Internship-Completed-brightgreen.svg)
![Tests](https://img.shields.io/badge/Unit%20Tests-19%2F19%20Passing-success.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

This repository contains the complete implementation of all tasks assigned during the **Software Development Internship Program** at **Cognifyz Technologies** ("Where Data Meets Intelligence").

The tasks span beginner, intermediate, and advanced levels, adhering to modular, readable, object-oriented, and thoroughly tested Python practices.

---

## 📑 Table of Contents

- [Repository Structure](#-repository-structure)
- [Summary of Tasks](#-summary-of-tasks)
  - [Level 1: Beginner](#level-1-beginner)
    - [Task 1: Basic Text-Based Game](#task-1-basic-text-based-game)
    - [Task 2: Number Patterns Generator](#task-2-number-patterns-generator)
  - [Level 2: Intermediate](#level-2-intermediate)
    - [Task 3: Task Manager CRUD Console App](#task-3-task-manager-crud-console-app)
    - [Task 4: Temperature Converter Program](#task-4-temperature-converter-program)
  - [Level 3: Advanced](#level-3-advanced)
    - [Task 5: Persistent Task Manager with File I/O](#task-5-persistent-task-manager-with-file-io)
    - [Task 6: Interactive Web Scraping Program](#task-6-interactive-web-scraping-program)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [Running Automated Tests](#-running-automated-tests)
- [LinkedIn Submission Guidelines](#-linkedin-submission-guidelines)

---

## 📂 Repository Structure

```plaintext
Cognifyz-Software-Development-Internship/
│
├── Level-1/
│   ├── task1_text_based_game.py       # Task 1: Number Guessing Game & Tech Trivia Quiz
│   └── task2_number_patterns.py       # Task 2: Number patterns with loops
│
├── Level-2/
│   ├── task3_task_manager_crud.py     # Task 3: In-Memory Task CRUD application
│   └── task4_temperature_converter.py # Task 4: Multi-unit temperature converter
│
├── Level-3/
│   ├── task5_persistent_task_manager.py   # Task 5: File I/O Task Manager (JSON & TXT export)
│   └── task6_interactive_web_scraper.py   # Task 6: Interactive web scraper (BeautifulSoup)
│
├── tests/
│   └── test_all_tasks.py              # Comprehensive automated unit & integration test suite
│
├── main.py                            # Unified interactive dashboard / runner
├── requirements.txt                   # External dependencies
├── .gitignore                         # Git exclusion rules
└── README.md                          # Project documentation
```

---

## 🎯 Summary of Tasks

### Level 1: Beginner

#### Task 1: Basic Text-Based Game
- **File**: `Level-1/task1_text_based_game.py`
- **Objective**: Implement a simple game using conditional statements for game logic.
- **Key Features**:
  - **Number Guessing Game**: Features 3 configurable difficulty tiers (Easy, Medium, Hard), dynamic range generation, attempt countdown, adaptive distance hints ("Hot", "Warm", "Cold"), and scoring logic.
  - **Software Engineering Trivia Quiz**: 5-question multi-choice quiz testing core software concepts (OOP, Data Structures, Time Complexity, Exceptions) with real-time feedback, explanations, and final grade calculation.
  - Input validation to handle non-numeric inputs and premature exit requests.

#### Task 2: Number Patterns Generator
- **File**: `Level-1/task2_number_patterns.py`
- **Objective**: Utilize loops (nested `for` and `while`) to control the structure of number patterns.
- **Supported Patterns**:
  1. *Half Pyramid (Right-Angled Triangle)*
  2. *Inverted Half Pyramid*
  3. *Full Centered Symmetrical Pyramid*
  4. *Floyd's Triangle (Sequential continuous integers)*
  5. *Pascal's Triangle (Binomial coefficient logic)*
  6. *Diamond Number Pattern*
  7. *Complete Pattern Showcase Mode*

---

### Level 2: Intermediate

#### Task 3: Task Manager CRUD Console App
- **File**: `Level-2/task3_task_manager_crud.py`
- **Objective**: Implement Create, Read, Update, and Delete operations using arrays/lists for data storage.
- **Key Features**:
  - Structured `Task` class containing `task_id`, `title`, `description`, `status` (*Pending*, *In Progress*, *Completed*), `priority` (*Low*, *Medium*, *High*), and `created_at`.
  - In-memory `TaskManager` maintaining tasks in a standard Python list.
  - CRUD Operations:
    - **Create**: Add new task with validation.
    - **Read**: Formatted tabular display, fetch by unique ID, keyword search, status/priority filtering.
    - **Update**: In-place field updates without overwriting untouched attributes.
    - **Delete**: Remove task with user confirmation guard.
  - Seed function to populate sample tasks instantly for evaluation.

#### Task 4: Temperature Converter Program
- **File**: `Level-2/task4_temperature_converter.py`
- **Objective**: Enable users to input temperatures and choose conversion direction between Fahrenheit and Celsius (plus Kelvin).
- **Supported Conversions**:
  - Celsius to Fahrenheit ($F = \frac{9}{5}C + 32$)
  - Fahrenheit to Celsius ($C = (F - 32) \times \frac{5}{9}$)
  - Celsius $\leftrightarrow$ Kelvin ($K = C + 273.15$)
  - Fahrenheit $\leftrightarrow$ Kelvin
- **Key Features**:
  - Physical boundary validation guarding against values below **Absolute Zero** ($-273.15^\circ\text{C}$, $-459.67^\circ\text{F}$, $0\text{ K}$).
  - Benchmark reference guide (Freezing point, Body temp, Boiling point).
  - Session conversion history tracker.

---

### Level 3: Advanced

#### Task 5: Persistent Task Manager with File I/O
- **File**: `Level-3/task5_persistent_task_manager.py`
- **Objective**: Implement file storage for tasks to enable saving and loading from a text/JSON file with robust error handling.
- **Key Features**:
  - Persistent JSON storage engine (`tasks_storage.json`) ensuring data survives process termination.
  - Automatic persistence on Create, Update, and Delete operations.
  - Human-readable text report exporter (`tasks_export.txt`).
  - Comprehensive Error Handling:
    - `FileNotFoundError`: Automatic safe initialization of fresh storage.
    - `json.JSONDecodeError`: Graceful handling of corrupted files with automatic creation of a dated `.bak` recovery file.
    - `PermissionError` and `OSError` safety handlers.

#### Task 6: Interactive Web Scraping Program
- **File**: `Level-3/task6_interactive_web_scraper.py`
- **Objective**: Fetch data from websites and present it in a user-friendly layout using a simple web scraping library (`BeautifulSoup` + `requests`).
- **Key Features**:
  - **Quotes Scraper**: Scrapes inspirational quotes, authors, and tags from `http://quotes.toscrape.com` with multi-page support.
  - **Books Catalogue Scraper**: Scrapes book titles, prices, ratings, and stock status from `http://books.toscrape.com`.
  - **Custom URL Analyzer**: Accepts any public web page URL and parses the Title, H1/H2 Headings, Paragraph highlights, and hyperlinks.
  - **Export Engine**: Export scraped results to both **JSON** and **CSV** formats with a single keystroke.
  - Network error handling for timeouts, invalid schemas, and HTTP error responses.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ksomesha13-cpu/Cognifyz-Software-Development-Internship.git
   cd Cognifyz-Software-Development-Internship
   ```

2. **Verify Python (3.8+ required):**
   ```bash
   python --version
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

### Method 1: Unified Interactive Dashboard (Recommended)
Launch the interactive task runner to select and run any task or the automated test suite from a single menu:
```bash
python main.py
```

### Method 2: Run Individual Tasks Directly

- **Task 1 (Game & Quiz):**
  ```bash
  python Level-1/task1_text_based_game.py
  ```

- **Task 2 (Number Patterns):**
  ```bash
  python Level-1/task2_number_patterns.py
  ```

- **Task 3 (In-Memory CRUD Task Manager):**
  ```bash
  python Level-2/task3_task_manager_crud.py
  ```

- **Task 4 (Temperature Converter):**
  ```bash
  python Level-2/task4_temperature_converter.py
  ```

- **Task 5 (Persistent File I/O Task Manager):**
  ```bash
  python Level-3/task5_persistent_task_manager.py
  ```

- **Task 6 (Interactive Web Scraper):**
  ```bash
  python Level-3/task6_interactive_web_scraper.py
  ```

---

## 🧪 Running Automated Tests

A comprehensive unit test suite is included in `tests/test_all_tasks.py` covering all tasks, edge cases, formulas, data transformations, and error handling.

Execute the test suite using:
```bash
python tests/test_all_tasks.py
```

**Test Output:**
```plaintext
test_guessing_game_bounds_and_attempts ... ok
test_trivia_quiz_evaluation ... ok
test_floyds_triangle ... ok
test_full_pyramid_and_diamond ... ok
test_half_pyramid ... ok
test_inverted_half_pyramid ... ok
test_pascals_triangle ... ok
test_create_and_read_task ... ok
test_get_by_id_and_search ... ok
test_update_and_delete_task ... ok
test_absolute_zero_exception ... ok
test_celsius_to_fahrenheit ... ok
test_convert_dispatcher ... ok
test_fahrenheit_to_celsius ... ok
test_kelvin_conversions ... ok
test_corrupted_file_handling ... ok
test_persistence_cycle ... ok
test_text_export ... ok
test_html_parser_mock ... ok

----------------------------------------------------------------------
Ran 19 tests in 0.057s

OK
```

---

## 📢 LinkedIn Submission Guidelines

As per Cognifyz Technologies internship rules:
1. **Video Showcase**: Record a short video demonstrating each task in action (using `python main.py`).
2. **Post on LinkedIn**: Share your achievements, certificate / offer letter, and project demo video.
3. **Tag Cognifyz**: Tag `@Cognifyz Technologies` in your post.
4. **Required Hashtags**:
   ```
   #cognifyztechnologies #cognifyz #cognifyztech #softwaredevelopment #python #internship
   ```

---

## 👨‍💻 Author

- **Intern Name**: Somesha K
- **GitHub**: [@ksomesha13-cpu](https://github.com/ksomesha13-cpu)
- **Organization**: Cognifyz Technologies
