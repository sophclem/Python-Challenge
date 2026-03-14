"""
File: num_analyze.py
Author: Sophie Clemens
Date: March 13, 2026

Description:
This program prompts the user to enter a numeric range and analyzes
each number in that range. The program categorizes numbers based on
a given set of properties and prints the results.

"""
import json
import sys

def is_prime(n):
    """
    Determines if a number is prime. 
    """
    if n < 2:
        return False
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    
    return True

def is_even(n):
    """
    Determines if a number is even. 
    """
    return n % 2 == 0

def is_odd(n):
    """
    Determines if a number is odd. 
    """
    return n % 2 != 0


BUILT_IN_RULES = {
    "even": is_even,
    "odd": is_odd,
    "prime": is_prime
}

def load_config(filename):
    """
    Load the config file and check that it is formatted correctly.
    Args: Config file
    Returns: List of dictionaries containing rules
    """
    try:
        with open(filename, "r") as file:
            config = json.load(file)

            # confirm categories exists in config file
            if "categories" not in config:
                print("Error: Config must contain 'categories'.")
                sys.exit(1)

            return config["categories"]

    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' not found.")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON.")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error loading config: {e}")
        sys.exit(1)

def get_rule_function(rule_text):
    """
    Fetch the rule function for a given string (either function definition or name of existing function)
    Args: Rule name or definition
    Returns: Rule function
    """

    # determine if function exists already (odd, even or prime)
    if rule_text in BUILT_IN_RULES:
        return BUILT_IN_RULES[rule_text]

    if rule_text.startswith("lambda"):
        try:
            return eval(rule_text)
        except Exception:
            print(f"Error: Invalid rule definition: {rule_text}")
            sys.exit(1)

    # rule does not exist
    print(f"Unsupported rule: {rule_text}")
    sys.exit(1)

def prepare_categories(categories):
    """
    Validate category entries from the config file and convert each rule
    into a callable function.
    Args: List of category dictionaries
    Returns: A list of  category dictionaries with labels and callable functions.
    """
    prepared = []

    for category in categories:
        if "label" not in category:
            print("Error: Each category must contain 'label'.")
            sys.exit(1)

        if "rule" not in category:
            print("Error: Each category must contain 'rule'.")
            sys.exit(1)

        label = category["label"]
        rule_text = category["rule"]
        rule_func = get_rule_function(rule_text)

        prepared.append({
            "label": label,
            "func": rule_func
        })

    return prepared

def categorize_number(number, categories):
    """
    Determines which categories apply to a given number. 
    Args: Number; List of dictionaries containing rules
    Returns: List of categories for given number
    """
    matched_labels = []

    for category in categories:
        # catching errors such as dividing by 0
        try:
            if category["func"](number):
                matched_labels.append(category["label"])
        except Exception:
            print(f"Error evaluating rule: {category['label']}")
            sys.exit(1)

    return matched_labels

def main():
    """
    Prompts user for range and returns numbers followed by corresponding categories
    """
    categories = load_config("analyzer-config.json")
    prepared_categories = prepare_categories(categories)

    try:
        start = int(input("Enter start of range: "))
        end = int(input("Enter end of range: "))
    except ValueError:
        print("Error: Please enter valid integers for the range.")
        sys.exit(1)

    if start > end:
        print("Error: Start of range must be less than or equal to end of range.")
        sys.exit(1)

    for number in range(start, end + 1):
        labels = categorize_number(number, prepared_categories)
        print(f"{number}: {', '.join(labels)}")


if __name__ == "__main__":
    main()