from django.contrib import admin
import nested_admin

from .models import Survey, Question, Option


class OptionAdminInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 1


class QuestionAdminInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1
    inlines = (OptionAdminInline,)


@admin.register(Survey)
class SurveyAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description', 'date_start', 'date_end')
    list_filter = ('title', 'date_start', 'date_end')

    inlines = [QuestionAdminInline]

    def get_readonly_fields(self, request, obj=None):
        return ['date_start'] if obj else []