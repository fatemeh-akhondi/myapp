from django.db import models

class Question(models.Model):
	title = models.CharField(max_length=200)
	statement = models.CharField(max_length=200)
	
	def __str__(self):
		return self.title
class TestCase(models.Model):
	input = models.TextField(blank=True)
	expected_output = models.TextField()
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='testCases')
 
	def __str__(self):
		return  "test_case_" + str(self.id) + "_" + self.question.title