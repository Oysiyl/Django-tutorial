from django.contrib import admin

# Register your models here.
# This allow you to change them from admin panel
from .models import Question
from .models import Choice

# Model for Question
admin.site.register(Question)
# Model for Choice
admin.site.register(Choice)
