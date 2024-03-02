from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from django.db.models import Q

from ..models import Question, Advertisement

from django.contrib.auth.decorators import login_required

from common.models import User

from django.utils import timezone

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    popular_questions = Question.objects.order_by('-voter')[:5]
    advertisement_first = Advertisement.objects.all()[0]
    advertisement_second = Advertisement.objects.all()[1]
    advertisement_last = Advertisement.objects.all()[2]
    today = timezone.now().date()
    daily_users_count = User.objects.filter(last_login__date=today).count()
    users_count = User.objects.all().count()

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'popular_questions': popular_questions, 'page': page, 'kw': kw, 'advertisement_first':advertisement_first, 'advertisement_second':advertisement_second, 'advertisement_last':advertisement_last, 'daily_users_count':daily_users_count, 'users_count':users_count,}
    return render(request, 'pybo/question_list.html', context)

@login_required(login_url='common:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

