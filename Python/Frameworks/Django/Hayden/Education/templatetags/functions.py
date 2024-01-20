from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def unslugify(value):
    """
    Convert a slug into a title.
    For example, 'hello-world' becomes 'Hello World'.
    """
    return value.replace('-', ' ').title()


@register.filter
@stringfilter
def roman_numerals(value):
    """
    Convert Arabic numerals to Roman numerals.
    For example, '1' becomes 'I', '2' becomes 'II', and so on.
    """
    numeral_map = {
        '1': 'I',
        '2': 'II',
        '3': 'III',
        '4': 'IV',
        '5': 'V'
    }

    result = ""

    for char in value:
        result += numeral_map.get(char, char)

    return result


def convert_to_gpa_and_letter_grade(Credit):
    """
    Convert the credit's letter grade and raw score grade to GPA and weighted GPA.
    """
    gpa_mapping = {
        'A+': 4.33,
        'A': 4.00,
        'A-': 3.67,
        'B+': 3.33,
        'B': 3.00,
        'B-': 2.67,
        'C+': 2.33,
        'C': 2.00,
        'C-': 1.67,
        'D+': 1.33,
        'D': 1.00,
        'D-': 0.67,
        'F': 0.00
    }

    gpa = gpa_mapping.get(Credit.letter_grade, 0.00)
    weighted_gpa = gpa + 1 if Credit.required_exam == "AP" else gpa

    score_to_grade_mapping = {
        97.00: "A+",
        93.00: "A",
        90.00: "A-",
        87.00: "B+",
        83.00: "B",
        80.00: "B-",
        77.00: "C+",
        73.00: "C",
        70.00: "C-",
        67.00: "D+",
        63.00: "D",
        60.00: "D-",
    }

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
