from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def unslugify(value):
    """
    Convert a slug into a title.
    For example, 'hello-world' becomes 'Hello World'.
    """
    return value.replace('-', ' ').title()


@register.filter
def roman_numerals(value):
    """
    Convert Arabic numerals to Roman numerals.
    For example, '1' becomes 'I', '2' becomes 'II', and so on.
    """
    numeral_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V'}
    result = "".join(numeral_map.get(char, char) for char in value)
    return result


def convert_to_gpa_and_letter_grade(Credit):
    """
    Convert the credit's letter grade and raw score grade to GPA and weighted GPA.
    """
    score_to_grade_mapping = {
        90.00: 4.00,
        89.00: 3.90,
        88.00: 3.80,
        87.00: 3.70,
        86.00: 3.50,
        85.00: 3.40,
        84.00: 3.30,
        83.00: 3.00,
        82.00: 2.90,
        81.00: 2.80,
        80.00: 2.70,
        79.00: 2.50,
        78.00: 2.40,
        77.00: 2.30,
        76.00: 2.10,
        75.00: 1.90,
        74.00: 1.80,
        73.00: 1.70,
        72.00: 1.50,
        71.00: 1.40,
        70.00: 1.30,
        69.00: 0.00
    }

    gpa_mapping = {
        4.33: 'A+',
        4.00: 'A',
        3.67: 'A-',
        3.33: 'B+',
        3.00: 'B',
        2.67: 'B-',
        2.33: 'C+',
        2.00: 'C',
        1.67: 'C-',
        1.33: 'D+',
        1.00: 'D',
        0.67: 'D-',
        0.00: 'F'
    }

    gpa = gpa_mapping.get(Credit.letter_grade, 0.00)
    weighted_gpa = gpa + 1 if Credit.required_exam == "AP" else gpa

    for grade, score in score_to_grade_mapping.items():
        if Credit.raw_score_grade >= grade:
            letter_grade = score
            break
    else:
        letter_grade = "F"

    return gpa, weighted_gpa, letter_grade


def is_college_credit_eligible(Credit):
    """
    Check if the credit is eligible for college credit based on the required exam.
    """
    return Credit.required_exam in {"AP", "CLEP"}


def is_registered(Credit):
    """
    Check if the credit is registered or not.
    """
    return Credit.registered


def is_upperschool(Credit):
    """
    Check if the credit belongs to upper school grade levels (FRESHMAN, SOPHOMORE, JUNIOR, SENIOR).
    """
    return Credit.grade_level in {Credit.FRESHMAN, Credit.SOPHOMORE, Credit.JUNIOR, Credit.SENIOR}


def calculate_net_cost(Institution):
    """
    Calculate the net cost by subtracting financial aid awarded from the next year's full tuition.
    """
    return Institution.next_year_full_tuition - Institution.financial_aid_awarded
