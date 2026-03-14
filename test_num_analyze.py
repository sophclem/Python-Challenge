import unittest
import tempfile
import os
from num_analyze import (
    is_even,
    is_odd,
    is_prime,
    get_rule_function,
    categorize_number, 
    load_config
)


class TestNumberAnalyzer(unittest.TestCase):

    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(3))

    def test_is_odd(self):
        self.assertTrue(is_odd(1))
        self.assertTrue(is_odd(3))
        self.assertFalse(is_odd(4))

    def test_is_prime(self):
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))

    def test_get_rule_function_builtin(self):
        even_rule = get_rule_function("even")
        odd_rule = get_rule_function("odd")
        prime_rule = get_rule_function("prime")

        self.assertTrue(even_rule(2))
        self.assertFalse(even_rule(1))

        self.assertTrue(odd_rule(1))
        self.assertFalse(odd_rule(2))

        self.assertTrue(prime_rule(13))
        self.assertFalse(prime_rule(4))

    def test_get_rule_function_lambda(self):
        div_by_3 = get_rule_function("lambda x: x % 3 == 0")

        self.assertTrue(div_by_3(9))
        self.assertFalse(div_by_3(10))

    def test_get_rule_function_invalid_lambda(self):
        with self.assertRaises(SystemExit):
            get_rule_function("lambda x x % 3 == 0")


    def test_categorize_number(self):
        categories = [
            {"label": "Even", "func": get_rule_function("even")},
            {"label": "Prime", "func": get_rule_function("prime")},
            {"label": "DivBy3", "func": get_rule_function("lambda x: x % 3 == 0")},
            {"label": "Odd", "func": get_rule_function("odd")},
        ]

        self.assertEqual(categorize_number(10, categories), ["Even"])
        self.assertEqual(categorize_number(11, categories), ["Prime", "Odd"])
        self.assertEqual(categorize_number(12, categories), ["Even", "DivBy3"])
        self.assertEqual(categorize_number(15, categories), ["DivBy3", "Odd"])

    def test_load_config_file_not_found(self):
        with self.assertRaises(SystemExit):
            load_config("does_not_exist.json")

    def test_load_config_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp:
            temp.write('{"categories": [}')
            temp_name = temp.name

        try:
            with self.assertRaises(SystemExit):
                load_config(temp_name)
        finally:
            os.remove(temp_name)

    def test_load_config_missing_categories(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp:
            temp.write('{"rule": []}')
            temp_name = temp.name

        try:
            with self.assertRaises(SystemExit):
                load_config(temp_name)
        finally:
            os.remove(temp_name)

    def test_get_rule_function_invalid_lambda(self):
        with self.assertRaises(SystemExit):
            get_rule_function("lambda x x % 3 == 0")

    def test_get_rule_function_unsupported_rule(self):
        with self.assertRaises(SystemExit):
            get_rule_function("divisible_by_3")

    def test_categorize_number_invalid_rule_in_category(self):
        categories = [
            {"label": "BadRule", "rule": "not_a_real_rule"}
        ]
        with self.assertRaises(SystemExit):
            categorize_number(5, categories)


if __name__ == "__main__":
    unittest.main()