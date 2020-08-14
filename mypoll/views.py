from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join(q.question_text for q in latest_question_list)
    # template = loader.get_template('mypoll/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }

    # return render(request, 'mypoll/index.html', context)
    # return HttpResponse(template.render(context, request))
    template_name = 'mypoll/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'mypoll/detail.html', {'question':question})
    # return HttpResponse("you are looking at question %s." % question_id)


def results(request, question_id):
    # response = "you are looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'mypoll/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'mypoll/detail.html', {
            "question":question,
            "error_message":"you didn't select a choice"
        })
    else:
        selected.votes += 1
        selected.save()

    return HttpResponseRedirect(reverse('mypoll:results', args=(question.id,) ))