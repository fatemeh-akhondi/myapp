from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CodeForm, LoginForm, SignupForm
from .models import Question
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from django.views import generic

import subprocess

class QuestionView:
	def question_bank(request):
		return render(request, "testit/question-bank.html", {"questions" : Question.objects.all()})
	
	@classmethod
	def question_detail(cls, request, id):
		question = Question.objects.get(id=id)

		if request.method == "POST":
			return redirect("testit:question_editor", id=id)

		return render(request, "testit/editor.html", {
			"question": question,
			"show_editor": False,
		})
  
	@classmethod
	def question_editor(cls, request, id):
		if (request.user.is_authenticated == False):
			return redirect("testit:login")

		question = Question.objects.get(id=id)
		success = False
		wrong_test_case = -1
  
		if request.method == "POST":
			form = CodeForm(request.POST)
   
			for test_case in question.testCases.all():
				output = Utils.run_code(request.POST, test_case.input)

				if (output.strip() != test_case.expected_output):
					wrong_test_case = test_case.get_question_group_id()
					break

			if (wrong_test_case == -1):
					success = True
					
		else:
			form = CodeForm()
			success = None
			
		return render(request, "testit/editor.html", {
			"question": question,
			"form" : form,
			"show_code_form" : True,
			"show_editor": False,
			"success" : success,
			"wrong_test_case" : wrong_test_case
		})

class Utils:
	@classmethod
	def run_code(cls, post_data, current_input):
		output = ""
		
		form = CodeForm(post_data)
		if form.is_valid():
			code = form.cleaned_data["code"]
			try:
				result = subprocess.run(
					["python3", "-c", code],
					input = current_input,
					capture_output=True,
					text=True,
					timeout=5
				)
				output = result.stdout + result.stderr
			except subprocess.TimeoutExpired:
				output = "Error: Execution timed out."
			except Exception as e:
				output = f"Error: {str(e)}"
				
		return output

class DetailView(generic.DetailView):
    model = Question
    template_name = "testit/editor.html"
		
def index(request):
	return render(request, "testit/index.html")

def editor_view(request):
	output = ""
	if request.method=="POST":
		form = CodeForm(request.POST)
		output = Utils.run_code(request.POST, form.cleaned_data["user_input"])
	else:
		form = CodeForm()

	return render(request, "testit/editor.html", {
		"form": form,
		"output": output,
		"show_editor": True,
		"no_expected": True,
	})

def logout_view(request):
	logout(request)
	return redirect("testit:index")
	# return HttpResponseRedirect(reverse("polls:index"))

def login_view(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("testit:index")
			else:
				return render(request, "testit/login.html", {
					"form" : LoginForm()
				})
	return render(request, "testit/login.html", {
			"form" : LoginForm(),
		}) 
  
def signup_view(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = User.objects.create_user(username=username, password=password)
			user.save()
			return redirect("testit:login")
	else:
		form = SignupForm()

	return render(request, "testit/signup.html", {
		"form": form,
	})