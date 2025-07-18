from django.urls import path

from . import views
from .views import QuestionView

app_name =  "testit"

urlpatterns = [
	path("", views.index, name="index"),
    path("editor/", views.editor_view, name="editor"),
    path("question-bank/", QuestionView.question_bank, name="question_bank"),
    path("question-bank/<int:id>/", QuestionView.question_detail, name="question_detail"),
    path("question-bank/<int:id>/", views.DetailView.as_view(), name="question_detail"),
    path("question-bank/<int:id>/editor/", QuestionView.question_editor, name="question_editor"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/<int:id>/", views.profile, name="profile"),
]
