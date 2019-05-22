from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Question, Choice
from .forms import QuestionForm, EmailChangeForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from rest_framework import generics
from serializers import UserSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# Add a new views here


class UserListAPIView(generics.ListAPIView):  # try habr
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @login_required
def password_change(request, template="registration/password_change.html"):
    # form = PasswordChangeForm(user=request.user, data=request.POST)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse(('polls:index')))
        # else:
        #     return HttpResponseRedirect(reverse(("update_password")))
    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, template, args)


# @login_required
def email_change(request, template="registration/email_change.html"):
    if request.method == 'GET':
        form = EmailChangeForm(user=request.user)
    elif request.method == 'POST':
        form = EmailChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse(('polls:index')))
    else:
        form = EmailChangeForm(user=request.user)
    args = {'form': form}
    return render(request, template, args)


def question_new(request, template='polls/new_question.html'):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Unpack form values
            question_text = form.cleaned_data['question_text']
            choice_text_1 = form.cleaned_data['choice_text_1']
            choice_text_2 = form.cleaned_data['choice_text_2']
            choice_text_3 = form.cleaned_data['choice_text_3']
            # Create the User record
            q = Question(question_text=question_text, pub_date=timezone.now())
            q.save()
            q.choice_set.create(choice_text=choice_text_1, votes=0)
            q.choice_set.create(choice_text=choice_text_2, votes=0)
            q.choice_set.create(choice_text=choice_text_3, votes=0)

            # Create Subscriber Record
            # Process payment (via Stripe)
            # Auto login the user
            return HttpResponseRedirect(reverse(('polls:index')))
    else:
        form = QuestionForm()

    return render(request, template, {'form': form})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    # Old version
    # return HttpResponse("Hello, world. You're at the polls index.")
    # A new one without templates:
    '''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
    '''
    # With templates and render
    question_list = Question.objects.get_queryset().order_by('id')
    # paginator
    paginator = Paginator(object_list=question_list, per_page=1)  # Show 25 contacts per page
    # template = loader.get_template('polls/index.html')
    page = request.GET.get('page')
    latest_question_list = paginator.get_page(page)
    context = {
        'latest_question_list': latest_question_list
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # Without get_object_or_404
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    '''
    # With get_object_or_404
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be
        published in the future).
        """
        # Including future questions
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions tat aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    # Old version
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
