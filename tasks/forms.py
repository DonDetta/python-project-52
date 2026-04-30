from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['description'].label = 'Описание'
        self.fields['status'].label = 'Статус'
        self.fields['executor'].label = 'Исполнитель'
        self.fields['labels'].label = 'Метки'
        self.fields['executor'].label_from_instance = (
            lambda u: u.get_full_name() or u.get_username()
        )
