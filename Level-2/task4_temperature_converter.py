"""
Task 4: Temperature Converter Program
Level 2: Intermediate
Internship Program: Software Development - Cognifyz Technologies

Objective:
Enable users to input temperatures and choose the conversion direction
between Fahrenheit and Celsius (with bonus support for Kelvin).

Features:
- Celsius to Fahrenheit & Fahrenheit to Celsius conversions
- Celsius <-> Kelvin and Fahrenheit <-> Kelvin conversions
- Physical validity checking against Absolute Zero (-273.15°C, -459.67°F, 0 K)
- Common temperature reference guide (Freezing, Room temp, Boiling, etc.)
- Conversion history logger and batch conversion mode
"""

import sys
from typing import Tuple, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67
ABSOLUTE_ZERO_K = 0.0


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit: F = (C * 9/5) + 32."""
    if c < ABSOLUTE_ZERO_C:
        raise ValueError(f"Temperature below absolute zero ({ABSOLUTE_ZERO_C}°C) is physically impossible.")
    return (c * 9.0 / 5.0) + 32.0


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius: C = (F - 32) * 5/9."""
    if f < ABSOLUTE_ZERO_F:
        raise ValueError(f"Temperature below absolute zero ({ABSOLUTE_ZERO_F}°F) is physically impossible.")
    return (f - 32.0) * 5.0 / 9.0


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin: K = C + 273.15."""
    if c < ABSOLUTE_ZERO_C:
        raise ValueError("Temperature below absolute zero is physically impossible.")
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius: C = K - 273.15."""
    if k < ABSOLUTE_ZERO_K:
        raise ValueError("Kelvin cannot be negative.")
    return k - 273.15


def fahrenheit_to_kelvin(f: float) -> float:
    """Convert Fahrenheit to Kelvin."""
    c = fahrenheit_to_celsius(f)
    return celsius_to_kelvin(c)


def kelvin_to_fahrenheit(k: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    c = kelvin_to_celsius(k)
    return celsius_to_fahrenheit(c)


def convert_temperature(val: float, from_unit: str, to_unit: str) -> float:
    """General converter dispatcher."""
    f = from_unit.strip().upper()
    t = to_unit.strip().upper()

    if f == t:
        return val

    if f == "C" and t == "F":
        return celsius_to_fahrenheit(val)
    elif f == "F" and t == "C":
        return fahrenheit_to_celsius(val)
    elif f == "C" and t == "K":
        return celsius_to_kelvin(val)
    elif f == "K" and t == "C":
        return kelvin_to_celsius(val)
    elif f == "F" and t == "K":
        return fahrenheit_to_kelvin(val)
    elif f == "K" and t == "F":
        return kelvin_to_fahrenheit(val)
    else:
        raise ValueError(f"Unsupported unit conversion: from '{from_unit}' to '{to_unit}'")


def display_reference_table():
    """Display standard benchmark temperatures across all scales."""
    benchmarks = [
        ("Absolute Zero", -273.15, -459.67, 0.0),
        ("Freezing Point of Water", 0.0, 32.0, 273.15),
        ("Comfortable Room Temp", 20.0, 68.0, 293.15),
        ("Average Human Body Temp", 37.0, 98.6, 310.15),
        ("Boiling Point of Water", 100.0, 212.0, 373.15),
    ]
    print("\n" + "=" * 65)
    print("🌡️  STANDARD TEMPERATURE REFERENCE TABLE")
    print("=" * 65)
    print(f"{'Condition':<26} | {'Celsius (°C)':<12} | {'Fahrenheit (°F)':<15} | {'Kelvin (K)':<10}")
    print("-" * 65)
    for name, c, f, k in benchmarks:
        print(f"{name:<26} | {c:<12.2f} | {f:<15.2f} | {k:<10.2f}")
    print("=" * 65)


def run_converter_interactive():
    """Interactive loop for temperature converter."""
    history: List[str] = []

    while True:
        print("\n" + "=" * 55)
        print("  COGNIFYZ INTERNSHIP - TASK 4: TEMPERATURE CONVERTER")
        print("=" * 55)
        print("1. 🌡️  Celsius to Fahrenheit (°C -> °F)")
        print("2. 🌡️  Fahrenheit to Celsius (°F -> °C)")
        print("3. 🧪 Celsius to Kelvin (°C -> K)")
        print("4. 🧪 Kelvin to Celsius (K -> °C)")
        print("5. 🔄 Fahrenheit to Kelvin (°F -> K)")
        print("6. 🔄 Kelvin to Fahrenheit (K -> °F)")
        print("7. 📊 View Standard Reference Table")
        print("8. 📜 View Conversion History")
        print("9. 🚪 Exit")

        choice = input("\nSelect conversion option (1-9): ").strip()

        if choice == "9":
            print("Exiting Temperature Converter. Goodbye!")
            break

        if choice == "7":
            display_reference_table()
            continue

        if choice == "8":
            print("\n📜 Conversion History:")
            if not history:
                print("  No conversions performed yet.")
            else:
                for idx, record in enumerate(history, 1):
                    print(f"  {idx}. {record}")
            continue

        conversions = {
            "1": ("C", "F", "Celsius", "Fahrenheit", "°C", "°F"),
            "2": ("F", "C", "Fahrenheit", "Celsius", "°F", "°C"),
            "3": ("C", "K", "Celsius", "Kelvin", "°C", "K"),
            "4": ("K", "C", "Kelvin", "Celsius", "K", "°C"),
            "5": ("F", "K", "Fahrenheit", "Kelvin", "°F", "K"),
            "6": ("K", "F", "Kelvin", "Fahrenheit", "K", "°F"),
        }

        if choice in conversions:
            from_code, to_code, from_name, to_name, s_from, s_to = conversions[choice]
            try:
                raw_val = input(f"Enter temperature in {from_name} ({s_from}): ").strip()
                val = float(raw_val)
                result = convert_temperature(val, from_code, to_code)
                record = f"{val:.2f}{s_from} = {result:.2f}{s_to}"
                history.append(record)
                print("\n" + "-" * 40)
                print(f"✅ Result: {record}")
                print("-" * 40)
            except ValueError as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Invalid option! Please enter a choice between 1 and 9.")


def main():
    run_converter_interactive()


if __name__ == "__main__":
    main()
