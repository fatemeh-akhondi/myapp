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
		output = ""
		question = Question.objects.get(id=id)
		success = False
		
		if request.method == "POST":
			output = Utils.run_code(request.POST)

			form = CodeForm(request.POST)
			if (form.is_valid()):
				expected = form.cleaned_data["expected_output"]
			
				if (output.strip() == expected.strip()):
					success = True
					
		else:
			form = CodeForm()
			success = None
			
		return render(request, "testit/editor.html", {
			"question": question,
			"form": form,
			"output": output,
			"show_editor": True,
			"success" : success
		})

class Utils:
	@classmethod
	def run_code(cls, post_data):
		output = ""
		
		form = CodeForm(post_data)
		if form.is_valid():
			code = form.cleaned_data["code"]
			user_input = form.cleaned_data["user_input"]
			try:
				result = subprocess.run(
					["python3", "-c", code],
					input = user_input,
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
		output = Utils.run_code(request.POST)
	else:
		form = CodeForm()

	return render(request, "testit/editor.html", {
		"form": form,
		"output": output,
		"show_editor": True,
		"no_expected": True,
	})
