from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CodeForm
from .models import Question

import subprocess

class QuestionView:
	def question_bank(request):
		return render(request, "testit/question-bank.html", {"questions" : Question.objects.all()})
	
	@classmethod
	def question_detail(cls, request, id):
		question = Question.objects.get(id=id)

		if request.method == "POST":
			return redirect("question_editor", id=id)

		return render(request, "testit/editor.html", {
			"question": question,
			"show_editor": False,
		})
  
	@classmethod
	def question_editor(cls, request, id):
		question = Question.objects.get(id=id)
		success = False
		wrong_test_case = -1
  
		if request.method == "POST":
			form = CodeForm(request.POST)
   
			for test_case in question.testCases.all():
				output = Utils.run_code(request.POST, test_case.input)

				if (output.strip() != test_case.expected_output):
					wrong_test_case = test_case.id
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
		
def index(response):
	return HttpResponse("Hello, world. You're at the testit index.")

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
