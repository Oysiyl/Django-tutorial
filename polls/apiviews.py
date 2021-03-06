from datetime import datetime
from django.utils import timezone

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Question, Choice

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChoiceSerializer, VoteSerializer
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer
from .serializers import QuestionResultPageSerializer, ChoiceSerializerWithVotes
from django.shortcuts import get_object_or_404

import json

# @csrf_exempt
@api_view(['GET', 'POST'])
def questions_view(request):
    """
    API View.
    GET: See the question by id.
    POST: Create a question.
    """
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionListPageSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, question_id):
    """
    API View for operate with concrete question, selected by id.
    GET: question by id.
    PATCH: change question_text in question.
    DELETE: delete question.
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def choices_view(request, question_id):
    """
    API View for add a new choice in question, selected by id.
    POST: Create new choice with choice text in question.
    """
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def vote_view(request, question_id):
    """
    API View for add one vote for a selected choice in question, selected by question_id.
    PATCH: Increase number of votes by one for a selected choice.
    """
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
        choice.votes += 1
        choice.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_result_view(request, question_id):
    """
    API View for a view results by question, selected by question_id.
    """
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)
