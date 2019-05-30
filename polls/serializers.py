from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Choice
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField(max_length=200)
    # choice_text_1 = serializers.CharField(max_length=200, default='first choice')
    # choice_text_2 = serializers.CharField(max_length=200, default='second choice')
    # choice_text_3 = serializers.CharField(max_length=200, default='third choice')

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)


class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(default=timezone.now())
    was_published_recently = serializers.BooleanField(read_only=True)  # Serializer is smart enough to understand that was_published_recently is a method on Question

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
