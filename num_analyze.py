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

# Purpose: Determines if a number is prime by checking all divisors up to the 
#          sq root of the given number. 
# Input/output: Takes in a number, return True if prime, False if not prime
def is_prime(n):
    if n < 2:
        return False
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    
    return True

# Purpose: Determines if a number is even
# Input/output: Takes in a number, return True if even, False if odd
def is_even(n):
    return n % 2 == 0

# Purpose: Determines if a number is odd
# Input/output: Takes in a number, return False if even, True if odd
def is_odd(n):
    return n % 2 != 0


BUILT_IN_RULES = {
    "even": is_even,
    "odd": is_odd,
    "prime": is_prime
}

def load_config(filename):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
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
    if rule_text in BUILT_IN_RULES:
        return BUILT_IN_RULES[rule_text]

    if rule_text.startswith("lambda"):
        func = eval(rule_text)

        if not callable(func):
            raise ValueError(f"Rule is not callable: {rule_text}")

        return func

    raise ValueError(f"Unsupported rule: {rule_text}")

# Purpose: Determines which categories apply to a given number. 
# Input/output: Takes in a number, returns list of categories that apply to
#               the given number
def categorize_number(number, categories):
    matched_labels = []

    for category in categories:
        label = category["label"]
        rule_text = category["rule"]
        rule_func = get_rule_function(rule_text)

        if rule_func(number):
            matched_labels.append(label)

    return matched_labels

# Purpose: Prompts the user for a range and prints categories for all numbers
#          in the range
# Input/output: None
def main():
    categories = load_config("analyzer-config.json")
    

    start = int(input("Enter start of range: "))
    end = int(input("Enter end of range: "))

    if start > end:
        print("The end of the range must be greater than the start of the range.")
        return
        # should the program return or prompt again?

    for number in range(start, end + 1):
        labels = categorize_number(number, categories)
        print(f"{number}: {', '.join(labels)}")


if __name__ == "__main__":
    main()