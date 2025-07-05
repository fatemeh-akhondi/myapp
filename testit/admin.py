from django.contrib import admin

from .models import Question
from .models import TestCase

admin.site.register(Question)
admin.site.register(TestCase)