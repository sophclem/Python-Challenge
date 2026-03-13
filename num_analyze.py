"""
File: num_analyze.py
Author: Sophie Clemens
Date: March 13, 2026

Description:
This program prompts the user to enter a numeric range and analyzes
each number in that range. The program categorizes numbers based on
a given set of properties and prints the results.

"""

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

# Purpose: Determines which categories apply to a given number. 
# Input/output: Takes in a number, returns list of categories that apply to
#               the given number
def categorize_number(n):
    categories = []

    if n % 2 == 0:
        categories.append("Even")
    else:
        categories.append("Odd")

    if is_prime(n):
        categories.append("Prime")

    return categories

# Purpose: Prompts the user for a range and prints categories for all numbers
#          in the range
# Input/output: None
def main():
    start = int(input("Enter start of range: "))
    end = int(input("Enter end of range: "))

    if start > end:
        print("The end of the range must be greater than the start of the range.")
        return
        # should the program return or prompt again?

    for num in range(start, end + 1):
        categories = categorize_number(num)
        print(f"{num}: {', '.join(categories)}")


if __name__ == "__main__":
    main()