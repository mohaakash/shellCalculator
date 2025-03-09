# Scientific Calculator Shell

A versatile command-line scientific calculator with support for mathematical operations, unit conversions, variable assignment, function definition, currency exchange, and graphing.

## Features

*   **Basic Arithmetic:** Addition, subtraction, multiplication, division, exponentiation.
*   **Advanced Functions:** Trigonometric functions (sin, cos, tan, asin, acos, atan), logarithms (log, ln), square root (sqrt), exponential (exp), power (pow), root, factorial (fact).
*   **Number Base Conversion:** Convert between decimal, binary, hexadecimal, and octal number systems.
*   **Degree/Radian Conversion:** Convert between degrees and radians.
*   **Unit Conversions:** Supports various unit conversions for length, area, volume, weight, speed, pressure, power, and temperature.
    *   Length: cm to in, in to cm, m to ft, ft to m, km to mile, mile to km
    *   Area: acre to m^2, m^2 to acre
    *   Volume: gal(US) to L, L to gal(US)
    *   Weight: oz to g, g to oz
    *   Speed: km/h to m/s, m/s to km/h
    *   Pressure: atm to Pa, Pa to atm
    *   Power: hp to kW, kW to hp
    *   Temperature: F to C, C to F
*   **Currency Exchange:** Fetches real-time exchange rates for various currencies via an external API.
*   **Variable Assignment:** Store and reuse values with custom variable names.
*   **Function Definition:** Define custom functions and evaluate them.
*   **Function Graphing:** Generate simple graphs of defined functions.
*   **Last Answer:** `ans` variable stores the result of the last calculation.
*   **Clear screen:** clear the screen of the shell.
* **Delete saved variables:** delete all saved variables and functions.
*   **Error Handling:** Provides informative error messages for invalid input.
*   **Colorful Output:** Uses `colorama` for colored output (if available).
* **Logo:** show the cool project logo.
* **Exit:** exit by writing exit or quit.

## Getting Started

### Prerequisites

*   Python 3.x
*   The following Python packages:
    *   `requests` (for currency exchange)
    *   `matplotlib` (for graphing)
    *   `colorama` (for colored output - optional)

### Installation

1.  **Install Packages:**
    ```bash
    pip install requests matplotlib colorama
    ```

2.  **Run the Calculator:**
    ```bash
    python main.py
    ```

## Usage

### Basic Operations

