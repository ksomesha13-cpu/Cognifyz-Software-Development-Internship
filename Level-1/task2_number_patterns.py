"""
Task 2: Generate and Print Simple Number Patterns
Level 1: Beginner
Internship Program: Software Development - Cognifyz Technologies

Objective:
Utilize loops to control the structure of number patterns.

Patterns Included:
1. Half Pyramid (Right-Angled Triangle)
2. Inverted Half Pyramid
3. Full Centered Symmetrical Pyramid
4. Floyd's Triangle (Sequential Numbers)
5. Pascal's Triangle
6. Diamond Number Pattern
7. Showcase / Print All Patterns
"""
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_half_pyramid(rows: int) -> str:
    """
    Generate a half pyramid of numbers.
    Example (rows=4):
    1
    1 2
    1 2 3
    1 2 3 4
    """
    lines = []
    for i in range(1, rows + 1):
        row_nums = [str(j) for j in range(1, i + 1)]
        lines.append(" ".join(row_nums))
    return "\n".join(lines)


def generate_inverted_half_pyramid(rows: int) -> str:
    """
    Generate an inverted half pyramid.
    Example (rows=4):
    1 2 3 4
    1 2 3
    1 2
    1
    """
    lines = []
    for i in range(rows, 0, -1):
        row_nums = [str(j) for j in range(1, i + 1)]
        lines.append(" ".join(row_nums))
    return "\n".join(lines)


def generate_full_pyramid(rows: int) -> str:
    """
    Generate a full centered symmetrical pyramid.
    Example (rows=4):
          1
        1 2 1
      1 2 3 2 1
    1 2 3 4 3 2 1
    """
    lines = []
    for i in range(1, rows + 1):
        # Leading spaces
        leading_spaces = "  " * (rows - i)
        # Increasing part
        asc = [str(j) for j in range(1, i + 1)]
        # Decreasing part
        desc = [str(j) for j in range(i - 1, 0, -1)]
        row_str = " ".join(asc + desc)
        lines.append(leading_spaces + row_str)
    return "\n".join(lines)


def generate_floyds_triangle(rows: int) -> str:
    """
    Generate Floyd's Triangle with continuous sequential integers.
    Example (rows=4):
    1
    2 3
    4 5 6
    7 8 9 10
    """
    lines = []
    current_num = 1
    for i in range(1, rows + 1):
        row_nums = []
        for _ in range(i):
            row_nums.append(str(current_num))
            current_num += 1
        lines.append(" ".join(row_nums))
    return "\n".join(lines)


def generate_pascals_triangle(rows: int) -> str:
    """
    Generate Pascal's Triangle using binomial expansion logic.
    Example (rows=4):
         1
        1 1
       1 2 1
      1 3 3 1
    """
    triangle = []
    for i in range(rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)

    lines = []
    for i, row in enumerate(triangle):
        spaces = " " * (rows - i - 1)
        row_str = " ".join(str(val) for val in row)
        lines.append(spaces + row_str)
    return "\n".join(lines)


def generate_diamond_pattern(rows: int) -> str:
    """
    Generate a symmetrical Diamond pattern with numbers.
    Rows must be odd or will be adjusted to represent upper half height.
    """
    lines = []
    # Upper half + middle
    for i in range(1, rows + 1):
        spaces = "  " * (rows - i)
        nums = [str(j) for j in range(1, i + 1)]
        rev_nums = [str(j) for j in range(i - 1, 0, -1)]
        lines.append(spaces + " ".join(nums + rev_nums))
    # Lower half
    for i in range(rows - 1, 0, -1):
        spaces = "  " * (rows - i)
        nums = [str(j) for j in range(1, i + 1)]
        rev_nums = [str(j) for j in range(i - 1, 0, -1)]
        lines.append(spaces + " ".join(nums + rev_nums))
    return "\n".join(lines)


PATTERNS = {
    "1": ("Half Pyramid", generate_half_pyramid),
    "2": ("Inverted Half Pyramid", generate_inverted_half_pyramid),
    "3": ("Full Centered Pyramid", generate_full_pyramid),
    "4": ("Floyd's Triangle", generate_floyds_triangle),
    "5": ("Pascal's Triangle", generate_pascals_triangle),
    "6": ("Diamond Pattern", generate_diamond_pattern),
}


def print_all_patterns(rows: int = 5):
    """Showcase all patterns side-by-side or sequentially."""
    print("\n" + "=" * 60)
    print(f"🌟 SHOWCASE OF ALL NUMBER PATTERNS (Rows = {rows})")
    print("=" * 60)
    for key, (name, func) in PATTERNS.items():
        print(f"\n--- [{key}] {name} ---")
        print(func(rows))
    print("=" * 60)


def main():
    """Interactive loop for Task 2."""
    while True:
        print("\n" + "=" * 55)
        print("  COGNIFYZ INTERNSHIP - TASK 2: NUMBER PATTERNS")
        print("=" * 55)
        for key, (name, _) in PATTERNS.items():
            print(f"{key}. {name}")
        print("7. Showcase All Patterns (Default 5 rows)")
        print("8. Exit")

        choice = input("\nSelect a pattern option (1-8): ").strip()
        if choice == "8":
            print("Exiting Number Patterns program. Goodbye!")
            break
        elif choice == "7":
            try:
                r_in = input("Enter number of rows (default 5): ").strip()
                r = int(r_in) if r_in else 5
                if r < 1 or r > 20:
                    print("⚠️ Please choose rows between 1 and 20.")
                    continue
                print_all_patterns(r)
            except ValueError:
                print("❌ Invalid input! Using default 5 rows.")
                print_all_patterns(5)
        elif choice in PATTERNS:
            name, func = PATTERNS[choice]
            try:
                r = int(input(f"Enter number of rows for {name} (1 - 15): ").strip())
                if r < 1 or r > 20:
                    print("⚠️ Row count must be between 1 and 20.")
                    continue
                print(f"\n✨ Generated Pattern ({name}, {r} rows):\n")
                print(func(r))
            except ValueError:
                print("❌ Invalid input! Please enter an integer.")
        else:
            print("❌ Invalid choice! Please select an option between 1 and 8.")


if __name__ == "__main__":
    main()
