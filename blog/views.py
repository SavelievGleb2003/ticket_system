from django.shortcuts import render, get_object_or_404
from .models import TurnoverDocument
from django.http import Http404
# Create your views here.
TD = TurnoverDocument.published

def TD_list(request):
    all_documents = TD.all()
    return render(request, 'blog/TD/list.html', {'all_documents': all_documents})

def TD_detail(request, year, month, day, TD):
    single_documents = get_object_or_404(TurnoverDocument,
                                         status=TurnoverDocument.Status.PUBLISHED,
                                         slug=TD,
                                         publish__year=year,
                                         publish__month=month,
                                         publish__day=day)
    return render(request, 'blog/TD/detail.html', {'single_documents': single_documents})