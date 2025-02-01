from django.shortcuts import render, get_object_or_404
from .models import TurnoverDocument
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import ListView


class ListTD(ListView):
    queryset = TurnoverDocument.published.all()
    template_name = 'blog/TD/list.html'
    paginate_by = 5
    context_object_name = 'all_documents'
def TD_detail(request, year, month, day, TD):
    single_document = get_object_or_404(
        TurnoverDocument,
        status=TurnoverDocument.Status.PUBLISHED,
        slug=TD,
        publish_by__year=year,
        publish_by__month=month,
        publish_by__day=day
    )


    return render(request, 'blog/TD/detail.html', {'single_document': single_document})
