from django.shortcuts import render, get_object_or_404
from .models import TurnoverDocument
from django.http import Http404
# Create your views here.
TD = TurnoverDocument.published

def TD_list(request):
    all_documents = TD.all()
    return render(request, 'blog/TD/list.html', {'all_documents': all_documents})

def TD_detail(request, id):
    single_documents = get_object_or_404(TurnoverDocument, id=id, status=TurnoverDocument.Status.PUBLISHED)
    return render(request, 'blog/TD/detail', {'single_documents': single_documents})