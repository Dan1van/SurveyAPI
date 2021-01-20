from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from collections import defaultdict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Survey, Question, Answer, Option
from .serializers import SurveyListSerializer, SurveyDetailSerializer, AnswerCreateSerializer

survey_list_response = openapi.Response('Response description', SurveyListSerializer)
survey_detail_response = openapi.Response('Response description', SurveyDetailSerializer)


class SurveyListView(APIView):

    @swagger_auto_schema(
        security=[],
        responses={
            '200': survey_list_response,
            '400': 'Bad Request'
        },
        operation_id='List of active surveys',
        operation_description='Return a list of all the active surveys'
    )
    def get(self, request):
        surveys = Survey.objects.all()
        active_surveys = [survey for survey in surveys if survey.date_end > timezone.now()]
        serializer = SurveyListSerializer(active_surveys, many=True)
        return Response(serializer.data)


class SurveyDetailView(APIView):

    @swagger_auto_schema(
        security=[],
        responses={
            '200': survey_detail_response,
            '400': 'Bad Request'
        },
        operation_id='Detailed info about some survey',
        operation_description='Return a detailed info about some survey'
    )
    def get(self, request, pk):
        survey = Survey.objects.get(id=pk)
        serializer = SurveyDetailSerializer(survey)
        return Response(serializer.data)

    @swagger_auto_schema(
        security=[],
        responses={
            '200': survey_detail_response,
            '400': 'Bad Request'
        },
        operation_id='Answer the survey',
        operation_description='Post answer on survey into db'
    )
    def post(self, request, pk):
        """
        To post new answer use this format:

        {
            "data": {
                "user-id": 1,
                "survey-id": 1,
                "answers": {
                    "1": [1],         <--
                    "2": [5, 6],      <--                Key is question-id, value is a list with answer ids or custom text
                    "3": ["Example of answer"]   <--
                }
            }
        }
        """
        answer = AnswerCreateSerializer(data=request.data)
        if answer.is_valid(raise_exception=True):
            answer.save()
            return Response(answer.data, status=status.HTTP_201_CREATED)
        return Response(answer.data, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, user_id):
        answer_list = defaultdict(lambda: defaultdict(list))
        answers = Answer.objects.values('survey', 'question', 'option', 'text', 'created').filter(user_id=user_id)

        for answer in answers:
            survey = Survey.objects.get(pk=answer['survey'])
            question = Question.objects.get(pk=answer['question'])
            if answer['option']:
                option = Option.objects.get(pk=answer['option'])
                answer_list[survey.title][question.text].append(option.text)
            else:
                answer_list[survey.title][question.text].append(answer['text'])

        return Response(answer_list)
