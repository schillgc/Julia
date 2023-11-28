import universities


def validate_academic_institution(request):
    uni = universities.API()
    academic_institution_details = uni.lucky(name=request)
    return academic_institution_details
