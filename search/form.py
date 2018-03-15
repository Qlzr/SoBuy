from django import forms
from .models import Keyword

class KeywordForm(forms.ModelForm):
	class Meta:
		model = Keyword
		fields = ['word']


class SelectForm(forms.Form):
	website = forms.fields.ChoiceField(
		choices = ((1, '全部'),(2, '京东'),(3, '当当')),
		initial = 1,
		widget = forms.widgets.RadioSelect
		)
	sort = forms.fields.ChoiceField(
		choices = ((1, '综合'), (2, '价格升'), (3, '价格降')),
		initial = 1,
		widget = forms.widgets.RadioSelect
		)
		