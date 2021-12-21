def convert_to_weighted_gpa(Credit):
    if Credit.letter_grade == "A+":
        Credit.course_weighted_grade_point_average = 4.33
    elif Credit.letter_grade == "A":
        Credit.course_weighted_grade_point_average = 4.00
    elif Credit.letter_grade == "A-":
        Credit.course_weighted_grade_point_average = 3.67
    elif Credit.letter_grade == "B+":
        Credit.course_weighted_grade_point_average = 3.33
    elif Credit.letter_grade == "B":
        Credit.course_weighted_grade_point_average = 3.00
    elif Credit.letter_grade == "B-":
        Credit.course_weighted_grade_point_average = 2.67
    elif Credit.letter_grade == "C+":
        Credit.course_weighted_grade_point_average = 2.33
    elif Credit.letter_grade == "C":
        Credit.course_weighted_grade_point_average = 2.00
    elif Credit.letter_grade == "C-":
        Credit.course_weighted_grade_point_average = 1.67
    elif Credit.letter_grade == "D+":
        Credit.course_weighted_grade_point_average = 1.33
    elif Credit.letter_grade == "D":
        Credit.course_weighted_grade_point_average = 1.00
    elif Credit.letter_grade == "D-":
        Credit.course_weighted_grade_point_average = 0.67
    if Credit.required_exam == "AP":
        Credit.course_weighted_grade_point_average = Credit.course_weighted_grade_point_average + 1


def convert_to_letter_grade(Credit):
    if Credit.raw_score_grade >= 97.00:
        Credit.letter_grade = "A+"
    elif Credit.raw_score_grade >= 93.00:
        Credit.letter_grade = "A"
    elif Credit.raw_score_grade >= 90.00:
        Credit.letter_grade = "A-"
    elif Credit.raw_score_grade >= 87.00:
        Credit.letter_grade = "B+"
    elif Credit.raw_score_grade >= 83.00:
        Credit.letter_grade = "B"
    elif Credit.raw_score_grade >= 80.00:
        Credit.letter_grade = "B-"
    elif Credit.raw_score_grade >= 77.00:
        Credit.letter_grade = "C+"
    elif Credit.raw_score_grade >= 73.00:
        Credit.letter_grade = "C"
    elif Credit.raw_score_grade >= 70.00:
        Credit.letter_grade = "C-"
    elif Credit.raw_score_grade >= 67.00:
        Credit.letter_grade = "D+"
    elif Credit.raw_score_grade >= 63.00:
        Credit.letter_grade = "D"
    elif Credit.raw_score_grade >= 60.00:
        Credit.letter_grade = "D-"
    elif Credit.raw_score_grade < 60.00:
        Credit.letter_grade = "F"


def is_college_credit_eligible(Credit):
    return Credit.required_exam in {Credit.AP, Credit.CLEP}


def is_middleschool(Credit):
    return Credit.grade_level in {Credit.SIXTH_GRADE, Credit.SEVENTH_GRADE, Credit.EIGHTH_GRADE}


def is_registered(Credit):
    if Credit.registered:
        return Credit.registered


def is_upperschool(Credit):
    return Credit.grade_level in {Credit.FRESHMAN, Credit.SOPHOMORE, Credit.JUNIOR, Credit.SENIOR}


def net_cost(Institution):
    net_tuition = Institution.next_year_full_tuition - Institution.financial_aid_awarded
    return net_tuition
