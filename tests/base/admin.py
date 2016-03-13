# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Test, Question, Choice, UserTesting


class ChoiceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_count = 0
        right_count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                total_count += 1
                if form.cleaned_data.get('state_right'):
                    right_count += 1
        if right_count == 0:
            raise ValidationError('Должен быть хотя бы один правильный ответ!')
        if total_count == right_count:
            raise ValidationError('Все ответы не могут быть правильными!')


class ChoiceInline(admin.TabularInline):
    model = Choice
    formset = ChoiceFormSet


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)


admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(UserTesting)
