from django.shortcuts import render, get_object_or_404
from .models import TurnoverDocument
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import CommentForm, EmailTD_form
from django.core.mail import send_mail

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
    comments = single_document.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/TD/detail.html', {'single_document': single_document,'form': form, 'comments':comments})


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
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {Document.title}"
            )
            message = (
                f"Read {Document.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
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


def add_comment(request, id_d):
    document = get_object_or_404(TurnoverDocument, id=id_d,
                                 status=TurnoverDocument.Status.PUBLISHED)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.document = document
        comment.save()
    return render(request,
                  'blog/TD/Comment.html',{'document':document,'form':form, 'comment':comment})
