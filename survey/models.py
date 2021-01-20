from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название', help_text='Введите название опроса')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание опроса')
    date_start = models.DateTimeField(verbose_name='Время старта опроса')
    date_end = models.DateTimeField(verbose_name='Время окончания опроса')

    class Meta:
        ordering = ['title', '-date_start', '-date_end']

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_CHOICES = [
        (0, 'Один вариант ответа'),
        (1, 'Несколько вариантов ответа'),
        (2, 'Ответ текстом')
    ]

    text = models.CharField(max_length=120, verbose_name='Текст', help_text="Введите текст вопроса")
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='Тип', help_text='Выберите тип вопроса')
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.CharField(max_length=240, verbose_name='Текст', help_text='Введите текст вопроса')
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.IntegerField(verbose_name='ID пользователя')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True)
    text = models.TextField(verbose_name='Ответ на вопрос', null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


