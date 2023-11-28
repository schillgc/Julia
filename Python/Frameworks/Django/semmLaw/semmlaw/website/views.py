from django.template.response import TemplateResponse
from django.views.generic import DetailView
from .models import Attorney
from googlesearch import search


def get_news_search_results(Attorney):
    # Perform Google News search about the lawyer from the firm's webpage
    query = {
        Attorney.first_name,
        Attorney.last_name,
        "Schonekas, Evans, McGoey & McEachin, L.L.C."
    }
    search_results = search(query, num_results=100)

    # Return the search results
    return search_results


class Bio(DetailView):
    model = Attorney

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



def index(request, template_name="website/index.html"):
    return TemplateResponse(request, template_name)
