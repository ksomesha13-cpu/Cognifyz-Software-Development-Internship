"""
Cognifyz Technologies - Software Development Internship
Main Execution Dashboard & Task Runner

This central script allows you to launch and evaluate any of the internship
tasks (Levels 1 to 3) directly from one unified menu.
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add subdirectories to sys.path
sys.path.append(os.path.join(PROJECT_ROOT, "Level-1"))
sys.path.append(os.path.join(PROJECT_ROOT, "Level-2"))
sys.path.append(os.path.join(PROJECT_ROOT, "Level-3"))


def banner():
    print("""
========================================================================
   ____                  _  __            _____         _      
  / ___|___   __ _ _ __ (_)/ _|_   _     |_   _|__  ___| |__   
 | |   / _ \ / _` | '_ \| | |_| | | |______| |/ _ \/ __| '_ \  
 | |__| (_) | (_| | | | | |  _| |_| |______| |  __/ (__| | | | 
  \____\___/ \__, |_| |_|_|_|  \__, |      |_|\___|\___|_| |_| 
             |___/             |___/                           
        SOFTWARE DEVELOPMENT INTERNSHIP PROGRAM - TASK SUITE
========================================================================
    """)


def menu():
    print("Select a task to run:")
    print("------------------------------------------------------------------------")
    print("  [LEVEL 1: BEGINNER]")
    print("    1. Task 1: Basic Text-Based Game (Guessing Game & Trivia Quiz)")
    print("    2. Task 2: Number Patterns Generator (Pyramid, Floyd's, Pascal's)")
    print()
    print("  [LEVEL 2: INTERMEDIATE]")
    print("    3. Task 3: Task Manager CRUD Console App (In-Memory)")
    print("    4. Task 4: Temperature Converter (°C, °F, Kelvin + History)")
    print()
    print("  [LEVEL 3: ADVANCED]")
    print("    5. Task 5: Persistent Task Manager (File I/O, JSON Storage & Export)")
    print("    6. Task 6: Interactive Web Scraper (BeautifulSoup, Quotes, Books)")
    print()
    print("  [AUTOMATED TESTING & VERIFICATION]")
    print("    7. Run Complete Automated Test Suite (Unit & Integration Tests)")
    print("    8. Exit")
    print("------------------------------------------------------------------------")


def run_script(rel_path):
    full_path = os.path.join(PROJECT_ROOT, rel_path)
    if not os.path.exists(full_path):
        print(f"❌ File not found: {full_path}")
        return
    print(f"\n🚀 Launching {rel_path}...\n")
    try:
        subprocess.run([sys.executable, full_path], check=False)
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user.")


def main():
    while True:
        banner()
        menu()
        choice = input("Enter option (1-8): ").strip()
        if choice == "1":
            run_script(os.path.join("Level-1", "task1_text_based_game.py"))
        elif choice == "2":
            run_script(os.path.join("Level-1", "task2_number_patterns.py"))
        elif choice == "3":
            run_script(os.path.join("Level-2", "task3_task_manager_crud.py"))
        elif choice == "4":
            run_script(os.path.join("Level-2", "task4_temperature_converter.py"))
        elif choice == "5":
            run_script(os.path.join("Level-3", "task5_persistent_task_manager.py"))
        elif choice == "6":
            run_script(os.path.join("Level-3", "task6_interactive_web_scraper.py"))
        elif choice == "7":
            run_script(os.path.join("tests", "test_all_tasks.py"))
        elif choice == "8":
            print("\nThank you for using the Cognifyz Task Suite! Good luck with your submission! 🎉\n")
            break
        else:
            print("\n❌ Invalid choice! Please select an option between 1 and 8.\n")
        
        input("\nPress [Enter] to return to the main dashboard menu...")


if __name__ == "__main__":
    main()
