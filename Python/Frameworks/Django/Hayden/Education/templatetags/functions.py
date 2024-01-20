from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def unslugify(value):
    return value.replace('-', ' ').capitalize()


@register.filter
@stringfilter
def roman_numerals(value):
    return value.replace("1","I").replace("2","II").replace("3","III").replace("4","IV").replace("5","V")


def convert_to_gpa_and_letter_grade(Credit):
    gpa = 0.0
    if Credit.letter_grade == "A+":
        gpa = 4.33
    elif Credit.letter_grade == "A":
        gpa = 4.00
    elif Credit.letter_grade == "A-":
        gpa = 3.67
    elif Credit.letter_grade == "B+":
        gpa = 3.33
    elif Credit.letter_grade == "B":
        gpa = 3.00
    elif Credit.letter_grade == "B-":
        gpa = 2.67
    elif Credit.letter_grade == "C+":
        gpa = 2.33
    elif Credit.letter_grade == "C":
        gpa = 2.00
    elif Credit.letter_grade == "C-":
        gpa = 1.67
    elif Credit.letter_grade == "D+":
        gpa = 1.33
    elif Credit.letter_grade == "D":
        gpa = 1.00
    elif Credit.letter_grade == "D-":
        gpa = 0.67

    weighted_gpa = gpa + 1 if Credit.required_exam == "AP" else gpa

    if Credit.raw_score_grade >= 97.00:
        letter_grade = "A+"
    elif Credit.raw_score_grade >= 93.00:
        letter_grade = "A"
    elif Credit.raw_score_grade >= 90.00:
        letter_grade = "A-"
    elif Credit.raw_score_grade >= 87.00:
        letter_grade = "B+"
    elif Credit.raw_score_grade >= 83.00:
        letter_grade = "B"
    elif Credit.raw_score_grade >= 80.00:
        letter_grade = "B-"
    elif Credit.raw_score_grade >= 77.00:
        letter_grade = "C+"
    elif Credit.raw_score_grade >= 73.00:
        letter_grade = "C"
    elif Credit.raw_score_grade >= 70.00:
        letter_grade = "C-"
    elif Credit.raw_score_grade >= 67.00:
        letter_grade = "D+"
    elif Credit.raw_score_grade >= 63.00:
        letter_grade = "D"
    elif Credit.raw_score_grade >= 60.00:
        letter_grade = "D-"
    elif Credit.raw_score_grade < 60.00:
        letter_grade = "F"

    return gpa, weighted_gpa, letter_grade

def is_college_credit_eligible(Credit):
    return Credit.required_exam in {"AP", "CLEP"}

def is_registered(Credit):
    return Credit.registered

def is_upperschool(Credit):
    return Credit.grade_level in {Credit.FRESHMAN, Credit.SOPHOMORE, Credit.JUNIOR, Credit.SENIOR}

def net_cost(Institution):
    return Institution.next_year_full_tuition - Institution.financial_aid_awarded
