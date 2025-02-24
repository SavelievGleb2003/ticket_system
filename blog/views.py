from django.shortcuts import render, get_object_or_404, redirect
from .models import TurnoverDocument
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import CommentForm, EmailTD_form
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from .models import Folder, TurnoverDocument
from account.models import Department
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


def folder_list(request, folder_id=None):
    if folder_id:
        parent_folder = get_object_or_404(Folder, id=folder_id)
        folders = parent_folder.subfolders.all()
        documents = parent_folder.documents.all()
    else:
        parent_folder = None
        folders = Folder.objects.filter(parent__isnull=True)
        documents = TurnoverDocument.objects.filter(folder__isnull=True)

    breadcrumbs = []
    temp = parent_folder
    while temp:
        breadcrumbs.insert(0, temp)
        temp = temp.parent

    return render(request, "folders/folder_list.html", {
        "parent_folder": parent_folder,
        "breadcrumbs": breadcrumbs,
        "folders": folders,
        "documents": documents,
    })



class ListTD(ListView):
    model = TurnoverDocument
    template_name = 'blog/TD/list.html'
    context_object_name = 'all_documents'
    paginate_by = 5

    def get_queryset(self):
        queryset = TurnoverDocument.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug) if tag_slug else None
        return context

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TurnoverDocument, Folder


@login_required
def user_documents_and_folders(request, folder_id=None):

    if folder_id:
        parent_folder = get_object_or_404(Folder, id=folder_id)
        folders = parent_folder.subfolders.all()
        documents = parent_folder.documents.all()
    else:
        parent_folder = None
        folders = Folder.objects.filter(parent__isnull=True, documents__author=request.user).distinct()
        documents = TurnoverDocument.objects.filter(folder__isnull=True, author=request.user)

    breadcrumbs = []
    temp = parent_folder
    while temp:
        breadcrumbs.insert(0, temp)
        temp = temp.parent

    return render(request, "folders/folder_list.html", {
        "parent_folder": parent_folder,
        "breadcrumbs": breadcrumbs,
        "folders": folders,
        "documents": documents,
    })



@login_required
def documents_by_department(request, folder_id=None):
    if request.user.department:
        department = get_object_or_404(Department, id=request.user.department.id)
    else:
        messages.error(request, "у пользователя нет отдела.")
        return redirect('TD:folder_list')
    if folder_id:
        parent_folder = get_object_or_404(Folder, id=folder_id)
        folders = parent_folder.subfolders.all()
        documents = parent_folder.documents.all()
    else:
        parent_folder = None
        folders = Folder.objects.filter(parent__isnull=True, documents__author__department=department, documents__status=TurnoverDocument.Status.PUBLISHED).distinct()
        documents = TurnoverDocument.objects.filter(folder__isnull=True, author__department=department)

    breadcrumbs = []
    temp = parent_folder
    while temp:
        breadcrumbs.insert(0, temp)
        temp = temp.parent

    return render(request, "folders/folder_list.html", {
        "parent_folder": parent_folder,
        "breadcrumbs": breadcrumbs,
        "folders": folders,
        "documents": documents,
    })




@login_required
def TD_detail(request, year, month, day, TD):
    single_document = get_object_or_404(
        TurnoverDocument,
        status=TurnoverDocument.Status.PUBLISHED,
        slug=TD,
        publish_by__year=year,
        publish_by__month=month,
        publish_by__day=day
    )
    comments = single_document.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/TD/detail.html', {'single_document': single_document,'form': form, 'comments':comments})



@login_required
def send_email(request, id_d):
    Document = get_object_or_404(TurnoverDocument, id=id_d,
                                 status=TurnoverDocument.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailTD_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                Document.get_absolute_url()
            )
            subject = (
                f"{request.user.username} ({request.user.email}) "
                f"recommends you read {Document.title}"
            )
            message = (
                f"Read {Document.title} at {post_url}\n\n"
                f"{request.user.username}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
        sent = True
    else:
        form = EmailTD_form()

    return render(request,'blog/TD/share.html',
                  {'Document':Document, 'form':form, 'sent':sent})

@login_required
def add_comment(request, id_d):
    document = get_object_or_404(TurnoverDocument, id=id_d,
                                 status=TurnoverDocument.Status.PUBLISHED)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.name = request.user.username
        comment.email = request.user.email
        comment.document = document
        comment.save()
    return render(request,
                  'blog/TD/Comment.html',{'document':document,'form':form, 'comment':comment})


