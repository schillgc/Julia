from .utils.news import api
import requests
import universities


def get_news(request):
    everything = api.get_everything(q=request)
    r = requests.get(everything)
    news = r.json()
    news_list = {'news': news['results']}
    return news_list


def validate_academic_institution(request):
    uni = universities.API()
    academic_institution_details = uni.lucky(name=request)
    return academic_institution_details
