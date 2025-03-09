import math
import sys
import re
import os
import requests
import matplotlib.pyplot as plt  # For graphing

# Check for color support
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = WHITE = CYAN = ''
    class Style:
        RESET_ALL = ''

# Define available functions
FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'log': math.log,
    'ln': math.log,  # Natural logarithm (base e)
    'sqrt': math.sqrt,
    'exp': math.exp,
    'pi': math.pi,
    'e': math.e,
    'pow': lambda x, n: x ** n,
    'root': lambda x, n: x ** (1 / n),
    'fact': math.factorial,
    'bin': lambda x: bin(int(x))[2:],
    'hex': lambda x: hex(int(x))[2:],
    'oct': lambda x: oct(int(x))[2:],
    'dec': lambda x: int(str(x), 0),
    'deg': lambda x: math.degrees(x),
    'rad': lambda x: math.radians(x)
}

# Define unit conversions
UNIT_CONVERSIONS = {
    "cm to in": lambda x: x / 2.54,
    "in to cm": lambda x: x * 2.54,
    "m to ft": lambda x: x * 3.28084,
    "ft to m": lambda x: x / 3.28084,
    "km to mile": lambda x: x * 0.621371,
    "mile to km": lambda x: x / 0.621371,
    "acre to m^2": lambda x: x * 4046.86,
    "m^2 to acre": lambda x: x / 4046.86,
    "gal(US) to L": lambda x: x * 3.78541,
    "L to gal(US)": lambda x: x / 3.78541,
    "oz to g": lambda x: x * 28.3495,
    "g to oz": lambda x: x / 28.3495,
    "km/h to m/s": lambda x: x / 3.6,
    "m/s to km/h": lambda x: x * 3.6,
    "atm to Pa": lambda x: x * 101325,
    "Pa to atm": lambda x: x / 101325,
    "hp to kW": lambda x: x * 0.7457,
    "kW to hp": lambda x: x / 0.7457,
    "F to C": lambda x: (x - 32) * 5/9,
    "C to F": lambda x: (x * 9/5) + 32
}

VARIABLES = {}  # Store user-defined variables
FUNCTIONS_DEFINED = {}  # Store user-defined functions
LAST_ANSWER = None  # Store last calculated answer

class Logo:
    @staticmethod
    def display():
        logo = f"""
        {Fore.CYAN}  __ _          _ _             _            _       _             
        {Fore.CYAN} / _\ |__   ___| | |   ___ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
        {Fore.CYAN} \ \| '_ \ / _ \ | |  / __/ _` | |/ __| | | | |/ _` | __/ _ \| '__|
        {Fore.CYAN} _\ \ | | |  __/ | | | (_| (_| | | (__| |_| | | (_| | || (_) | |   
        {Fore.CYAN} \__/_| |_|\___|_|_|  \___\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
        """
        print(logo)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_exchange_rate(from_currency, to_currency):
    """Fetches exchange rate from an API that supports BDT."""
    try:
        # Use an API that supports BDT (e.g., ExchangeRate-API)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        if "rates" in data and to_currency.upper() in data["rates"]:
            return data["rates"][to_currency.upper()]
        else:
            return None
    except Exception as e:
        return None

def strip_ansi_codes(text):
    """Removes ANSI color codes from a string."""
    ansi_escape = re.compile(r'\x1b\[([0-9;]*[mGKH])')
    return ansi_escape.sub('', text)

def evaluate_expression(expression):
    """Evaluates a mathematical expression safely, with variable and unit conversion support."""
    global LAST_ANSWER, VARIABLES, FUNCTIONS_DEFINED
    try:
        # Replace variables in the expression with their values
        for var_name, value in VARIABLES.items():
            expression = re.sub(rf'\b{var_name}\b', str(value), expression)
        
        # Replace 'ans' with the last calculated answer
        expression = expression.replace("ans", str(LAST_ANSWER) if LAST_ANSWER is not None else "0")
        
        # Handle function definition
        if "=" in expression and "==" not in expression:  # Avoid confusion with evaluation
            var_name, expr = map(str.strip, expression.split("=", 1))
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_ ]*$', var_name) or var_name in FUNCTIONS:
                return f"{Fore.RED}Error: Invalid variable or function name{Style.RESET_ALL}"
            
            # Check if the expression contains 'x' (indicating a function)
            if 'x' in expr:
                # Store the function as a lambda
                try:
                    FUNCTIONS_DEFINED[var_name] = lambda x, e=expr: eval(e, {"__builtins__": None}, {**FUNCTIONS, **VARIABLES, 'x': x})
                    return f"{Fore.YELLOW}Function '{var_name}(x)' defined.{Style.RESET_ALL}"
                except Exception as e:
                    return f"{Fore.RED}Error: Invalid function definition - {e}{Style.RESET_ALL}"
            else:
                # Evaluate the right-hand side of the assignment
                result = evaluate_expression(expr)
                if result.startswith(Fore.RED):  # If there's an error, return it
                    return result
                
                # Strip ANSI color codes and store the numeric value
                stripped_result = strip_ansi_codes(result)
                try:
                    VARIABLES[var_name] = float(stripped_result.split()[-1])  # Extract numeric value
                except ValueError:
                    return f"{Fore.RED}Error: Could not convert result to a number{Style.RESET_ALL}"
                return f"{Fore.YELLOW}{var_name} = {VARIABLES[var_name]}{Style.RESET_ALL}"
        
        # Handle function evaluation
        if expression.startswith("evaluate"):
            parts = expression.split()
            if len(parts) == 5 and parts[2] == "for" and parts[4] == "==":
                func_name = parts[1]
                var = parts[3]
                value = float(parts[5])
                if func_name in FUNCTIONS_DEFINED:
                    if var == 'x':
                        result = FUNCTIONS_DEFINED[func_name](value)
                        return f"{Fore.YELLOW}{func_name}({value}) = {result}{Style.RESET_ALL}"
                    elif var == 'y':
                        # Solve for x given y (requires numerical methods)
                        # For simplicity, we'll use a brute-force approach
                        def f(x):
                            return FUNCTIONS_DEFINED[func_name](x) - value
                        x_guess = 0
                        step = 0.1
                        tolerance = 1e-6
                        while abs(f(x_guess)) > tolerance:
                            x_guess += step
                        return f"{Fore.YELLOW}{func_name}({x_guess}) = {value}{Style.RESET_ALL}"
                    else:
                        return f"{Fore.RED}Error: Invalid variable '{var}'{Style.RESET_ALL}"
                else:
                    return f"{Fore.RED}Error: Function '{func_name}' not defined{Style.RESET_ALL}"
            else:
                return f"{Fore.RED}Error: Invalid evaluation syntax{Style.RESET_ALL}"
        
        # Handle graphing
        if expression.startswith("graph"):
            func_name = expression.split()[1]
            if func_name in FUNCTIONS_DEFINED:
                x_values = [i * 0.1 for i in range(-100, 101)]  # Generate x values from -10 to 10
                y_values = [FUNCTIONS_DEFINED[func_name](x) for x in x_values]
                plt.plot(x_values, y_values, label=f"{func_name}(x)")
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title(f"Graph of {func_name}(x)")
                plt.legend()
                plt.grid()
                plt.show()
                return f"{Fore.YELLOW}Graphing {func_name}(x){Style.RESET_ALL}"
            else:
                return f"{Fore.RED}Error: Function '{func_name}' not defined{Style.RESET_ALL}"
        
        # Currency conversion (check this first to avoid conflicts)
        match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]{3})\s+to\s+([a-zA-Z]{3})', expression, re.IGNORECASE)
        if match:
            amount, from_currency, to_currency = match.groups()
            rate = get_exchange_rate(from_currency, to_currency)
            if rate:
                converted_amount = float(amount) * rate
                return f"{Fore.YELLOW}{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}{Style.RESET_ALL}"
            else:
                return f"{Fore.RED}Error: Unable to fetch exchange rate for {from_currency} to {to_currency}{Style.RESET_ALL}"
        
        # Unit conversion
        match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z^0-9/()]+)\s+to\s+([a-zA-Z^0-9/()]+)', expression, re.IGNORECASE)
        if match:
            amount, from_unit, to_unit = match.groups()
            conversion_key = f"{from_unit} to {to_unit}"
            if conversion_key in UNIT_CONVERSIONS:
                converted_amount = UNIT_CONVERSIONS[conversion_key](float(amount))
                return f"{Fore.YELLOW}{amount} {from_unit} = {converted_amount} {to_unit}{Style.RESET_ALL}"
            else:
                return f"{Fore.RED}Error: Unsupported unit conversion '{conversion_key}'{Style.RESET_ALL}"
        
        # Regular mathematical expression
        result = eval(expression, {"__builtins__": None}, {**FUNCTIONS, **VARIABLES})
        LAST_ANSWER = result
        return f"{Fore.YELLOW}{result}{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}Error: {e}{Style.RESET_ALL}"

def main():
    Logo.display()
    print("Scientific Calculator Shell (type 'exit' to quit)")
    while True:
        try:
            expression = input(f"{Fore.GREEN}calc> {Fore.WHITE}").strip()
            if expression.lower() in ['exit', 'quit']:
                break
            elif expression.lower() in ['clear', 'clr', 'cls', 'ac']:
                clear_screen()
                Logo.display()
                print("Scientific Calculator Shell (type 'exit' to quit)")
                continue
            elif expression.lower() in ['delete', 'del', 'dlt']:
                VARIABLES.clear()
                FUNCTIONS_DEFINED.clear()
                clear_screen()
                Logo.display()
                print("Scientific Calculator Shell (type 'exit' to quit)")
                print(f"{Fore.RED}All stored variables and functions deleted.{Style.RESET_ALL}")
                continue
            if not expression:
                continue
            result = evaluate_expression(expression)
            print(result)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting calculator.")
            break

if __name__ == "__main__":
    main()