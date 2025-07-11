from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={"id": "code-editor"}))
    
    user_input = forms.CharField(
        required=False,
        label="Standard Input (used for input())",
        widget=forms.Textarea(attrs={"rows": 4})
    )
    
    expected_output = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4})
        )
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)