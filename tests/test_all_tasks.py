"""
Automated Test Suite for Cognifyz Software Development Internship Tasks
Tests Task 1 through Task 6 across Levels 1, 2, and 3.
"""

import os
import sys
import unittest
import tempfile
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Setup import paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Level-1"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Level-2"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Level-3"))

from task1_text_based_game import NumberGuessingGame, TriviaQuizGame
from task2_number_patterns import (
    generate_half_pyramid,
    generate_inverted_half_pyramid,
    generate_full_pyramid,
    generate_floyds_triangle,
    generate_pascals_triangle,
    generate_diamond_pattern,
)
from task3_task_manager_crud import Task, TaskManager
from task4_temperature_converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    convert_temperature,
    ABSOLUTE_ZERO_C,
)
from task5_persistent_task_manager import PersistentTaskManager
from task6_interactive_web_scraper import CustomWebScraper, BeautifulSoup


class TestTask1TextGame(unittest.TestCase):
    """Unit tests for Task 1: Number Guessing and Trivia Quiz."""

    def test_guessing_game_bounds_and_attempts(self):
        game = NumberGuessingGame(difficulty="1")  # 1 to 50, 10 attempts
        self.assertEqual(game.low, 1)
        self.assertEqual(game.high, 50)
        self.assertEqual(game.max_attempts, 10)

        # Out of bounds
        out_res = game.evaluate_guess(999)
        self.assertEqual(out_res["status"], "out_of_bounds")

        # Correct guess simulation
        secret = game.secret_number
        win_res = game.evaluate_guess(secret)
        self.assertEqual(win_res["status"], "correct")
        self.assertTrue(game.is_won)
        self.assertGreater(win_res["score"], 0)

    def test_trivia_quiz_evaluation(self):
        quiz = TriviaQuizGame()
        self.assertEqual(quiz.score, 0)

        # Question 0 answer is 'B' (Queue FIFO)
        res_correct = quiz.evaluate_answer(0, "B")
        self.assertTrue(res_correct["correct"])
        self.assertEqual(quiz.score, 1)

        # Incorrect answer
        res_incorrect = quiz.evaluate_answer(1, "Z")
        self.assertFalse(res_incorrect["correct"])
        self.assertEqual(quiz.score, 1)


class TestTask2NumberPatterns(unittest.TestCase):
    """Unit tests for Task 2: Number pattern generation loops."""

    def test_half_pyramid(self):
        pattern = generate_half_pyramid(3)
        expected = "1\n1 2\n1 2 3"
        self.assertEqual(pattern, expected)

    def test_inverted_half_pyramid(self):
        pattern = generate_inverted_half_pyramid(3)
        expected = "1 2 3\n1 2\n1"
        self.assertEqual(pattern, expected)

    def test_floyds_triangle(self):
        pattern = generate_floyds_triangle(3)
        lines = pattern.split("\n")
        self.assertEqual(lines[0], "1")
        self.assertEqual(lines[1], "2 3")
        self.assertEqual(lines[2], "4 5 6")

    def test_pascals_triangle(self):
        pattern = generate_pascals_triangle(3)
        self.assertIn("1", pattern)
        self.assertIn("1 1", pattern)
        self.assertIn("1 2 1", pattern)

    def test_full_pyramid_and_diamond(self):
        pyr = generate_full_pyramid(3)
        self.assertIn("1 2 3 2 1", pyr)
        dia = generate_diamond_pattern(3)
        self.assertIn("1 2 3 2 1", dia)


class TestTask3TaskManagerCRUD(unittest.TestCase):
    """Unit tests for Task 3: In-Memory CRUD operations."""

    def setUp(self):
        self.mgr = TaskManager()

    def test_create_and_read_task(self):
        t1 = self.mgr.create_task("Test Title", "Test Description", "High", "Pending")
        self.assertEqual(t1.task_id, 1)
        self.assertEqual(t1.title, "Test Title")
        self.assertEqual(len(self.mgr.read_all_tasks()), 1)

    def test_get_by_id_and_search(self):
        self.mgr.create_task("Write unit tests", "Testing CRUD", "High")
        self.mgr.create_task("Deploy app", "Production deployment", "Low")

        task = self.mgr.get_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Write unit tests")

        search_res = self.mgr.search_tasks("unit")
        self.assertEqual(len(search_res), 1)
        self.assertEqual(search_res[0].task_id, 1)

    def test_update_and_delete_task(self):
        t = self.mgr.create_task("Draft email", "To manager", "Medium")
        updated = self.mgr.update_task(t.task_id, title="Sent email", status="Completed")
        self.assertEqual(updated.title, "Sent email")
        self.assertEqual(updated.status, "Completed")

        del_res = self.mgr.delete_task(t.task_id)
        self.assertTrue(del_res)
        self.assertEqual(len(self.mgr.read_all_tasks()), 0)


class TestTask4TemperatureConverter(unittest.TestCase):
    """Unit tests for Task 4: Temperature formulas and validations."""

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0.0), 32.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(100.0), 212.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40.0), -40.0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32.0), 0.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212.0), 100.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40.0), -40.0)

    def test_kelvin_conversions(self):
        self.assertAlmostEqual(celsius_to_kelvin(0.0), 273.15)
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0)

    def test_convert_dispatcher(self):
        res = convert_temperature(25.0, "C", "F")
        self.assertAlmostEqual(res, 77.0)

    def test_absolute_zero_exception(self):
        with self.assertRaises(ValueError):
            celsius_to_fahrenheit(-300.0)


class TestTask5FilePersistence(unittest.TestCase):
    """Unit tests for Task 5: File I/O persistence and error recovery."""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_persistence_cycle(self):
        # Create manager 1 and add task
        mgr1 = PersistentTaskManager(storage_path=self.temp_file.name, auto_load=False)
        mgr1.create_task("Persistent Task 1", "Must survive restart", "High", "In Progress")
        mgr1.save_to_file()

        # Create manager 2 pointing to the same file
        mgr2 = PersistentTaskManager(storage_path=self.temp_file.name, auto_load=True)
        tasks = mgr2.read_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Persistent Task 1")
        self.assertEqual(tasks[0].status, "In Progress")

    def test_text_export(self):
        mgr = PersistentTaskManager(storage_path=self.temp_file.name, auto_load=False)
        mgr.create_task("Export Task", "Testing report", "Medium")

        export_file = self.temp_file.name + ".txt"
        success = mgr.export_to_text_file(export_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(export_file))

        with open(export_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Export Task", content)
            self.assertIn("COGNIFYZ INTERNSHIP", content)

        if os.path.exists(export_file):
            os.remove(export_file)

    def test_corrupted_file_handling(self):
        # Write corrupted JSON to file
        with open(self.temp_file.name, "w") as f:
            f.write("{ INVALID JSON CONTENT :::")

        mgr = PersistentTaskManager(storage_path=self.temp_file.name, auto_load=True)
        # Should gracefully start with empty list without crashing
        self.assertEqual(len(mgr.read_all_tasks()), 0)


class TestTask6WebScraper(unittest.TestCase):
    """Unit tests for Task 6: HTML Parsing."""

    def test_html_parser_mock(self):
        mock_html = """
        <html>
            <head><title>Test Page Title</title></head>
            <body>
                <h1>Main Heading</h1>
                <h2>Sub Heading</h2>
                <p>This is a paragraph for testing web scraping functionality.</p>
                <a href="https://example.com/test">Example Link</a>
            </body>
        </html>
        """
        soup = BeautifulSoup(mock_html, "html.parser")
        self.assertEqual(soup.title.string.strip(), "Test Page Title")
        self.assertEqual(soup.find("h1").get_text().strip(), "Main Heading")
        self.assertEqual(soup.find("h2").get_text().strip(), "Sub Heading")
        self.assertIn("testing web scraping", soup.find("p").get_text())


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 RUNNING COGNIFYZ INTERNSHIP AUTOMATED TEST SUITE")
    print("=" * 60)
    unittest.main(verbosity=2)
