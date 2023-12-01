from typing import List

DIGIT_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def read_calibration_lines(docuemnt_path: str) -> List[str]:
    return open(docuemnt_path).read().split("\n")


def strip_calibration_line(calibration_line: str, use_explicit_digits_only: bool) -> str:
    """Remove non-numeric strings from calibration, optionally replace spelled out digits with value"""
    translation_dictionary = {"": ""} if use_explicit_digits_only else DIGIT_MAP
    for key, val in translation_dictionary.items():
        # replace spelled out digit with value, padded by spelled out version in case of letter overlap
        # e.g. eightwothree
        calibration_line = calibration_line.replace(key, f"{key}{val}{key}")
    return "".join(char for char in calibration_line if char.isdigit())


def calculate_calibration_values(calibration_document: List[str], use_explicit_digits_only: bool = True) -> List[int]:
    stripped_values = [strip_calibration_line(line, use_explicit_digits_only) for line in calibration_document]
    return [int(f"{val[0]}{val[-1]}") for val in stripped_values]


# Tests
test_document = read_calibration_lines("inputs/day01/day01_test.txt")
test_calibration_vals = calculate_calibration_values(test_document)
assert test_calibration_vals == [12, 38, 15, 77]
assert sum(test_calibration_vals) == 142

test_document2 = read_calibration_lines("inputs/day01/day01_test2.txt")
test_calibration_vals2 = calculate_calibration_values(test_document2, use_explicit_digits_only=False)
assert test_calibration_vals2 == [29, 83, 13, 24, 42, 14, 76]
assert sum(test_calibration_vals2) == 281


# Part 1
calibration_document = read_calibration_lines("inputs/day01/day01.txt")
calibration_values = calculate_calibration_values(calibration_document)
print(f"PART 1: Sum of Calibration Values - {sum(calibration_values)}")

# Part 2
calibration_document2 = read_calibration_lines("inputs/day01/day01.txt")
calibration_values2 = calculate_calibration_values(calibration_document2, use_explicit_digits_only=False)
print(f"PART 2: Sum of Calibration Values - {sum(calibration_values2)}")
