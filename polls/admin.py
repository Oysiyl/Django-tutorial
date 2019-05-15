from django.contrib import admin

# Register your models here.
# This allow you to change them from admin panel
from .models import Question
from .models import Choice

#You can set TabularInline to more smaller space's required for Choices
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


# Model for Question
# Old
# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)
# Model for Choice (inefficient way)
# admin.site.register(Choice)
