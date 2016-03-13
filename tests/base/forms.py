# -*- coding: utf-8 -*-
from django import forms
from .models import Question


class QuestionForm(forms.Form):
    def __init__(self, question_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = Question.objects.get(id=question_id)
        self.fields['question'] = self._get_field_class(self.question)(
            required=True,
            label=self.question.text,
            queryset=self.question.choices.all()
        )

    def _get_field_class(self, instance):
        if instance.choices.filter(state_right=True).count() == 1:
            return forms.ModelChoiceField
        return forms.ModelMultipleChoiceField
