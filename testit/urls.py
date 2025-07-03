from django.urls import path

from . import views
from .views import QuestionView

urlpatterns = [
	path("index/", views.index),
    path("editor/", views.editor_view),
    path("question-bank/", QuestionView.question_bank, name="question_bank"),
    path("question-bank/<int:id>/", QuestionView.question_detail, name="question_detail"),
    path("question-bank/<int:id>/editor/", QuestionView.question_editor, name="question_editor"),
]
