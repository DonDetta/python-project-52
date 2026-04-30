from django import forms

from labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
