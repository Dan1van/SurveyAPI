from rest_framework import serializers
from drf_yasg import openapi

from .models import Survey, Question, Answer, Option


class OptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = Option
        fields = ('id', 'text')


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True, source='get_type_display')
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'options')


class SurveyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ('title', 'description')


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    date_start = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    date_end = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'questions', 'date_start', 'date_end')


class AnswerCreateSerializer(serializers.Serializer):

    data = serializers.JSONField()

    def save(self):
        print(self.data)
        user_id = self.data['data']['user-id']
        answers = self.data['data']['answers']
        survey_id = self.data['data']['survey-id']

        survey = Survey.objects.get(pk=survey_id)


        if not answers:
            raise serializers.ValidationError('Answers must be not null.')

        for question_id in answers:
            question = Question.objects.get(pk=question_id)
            options = answers[question_id]
            for option_id in options:
                if question.type == 2:  # if question type is text answer
                    text_answer = answers[question_id]
                    Answer(user_id=user_id, survey=survey, question=question, text=text_answer).save()
                else:
                    option = Option.objects.get(pk=option_id)
                    Answer(user_id=user_id, survey=survey, question=question, option=option).save()

