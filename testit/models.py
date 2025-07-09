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
		return  "test_case_" + str(self.get_question_group_id()) + "_" + self.question.title

	def get_question_group_id(self):
		all_test_cases = self.question.testCases.all()
  
		return list(all_test_cases).index(self) + 1