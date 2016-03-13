# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserTesting(models.Model):
    """
    Результат выполнения тестирования пользоателям
    """
    user = models.ForeignKey(User, verbose_name='Пользователь')
    test = models.ForeignKey('Test', verbose_name='Тест')
    passed_questions = models.ManyToManyField('Question', through='Question2UserTesting')
    state_done = models.BooleanField(verbose_name='Тест заврешоен', default=False)

    class Meta:
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'

    def __str__(self):
        return '%s / %s' % (self.user, self.test)

    def get_result(self):
        """
        return <кол-во правильных ответов>, <всего вопросов>, <процент правильных>
        """
        if self.state_done:
            total_count = self.test.questions.count()
            right_count = self.passed_questions.filter(
                question2usertesting__state_right=True).count()
            return (right_count, total_count, right_count / total_count * 100)
        return False

    def get_next_question(self):
        """
        Возвращает следующий вопрос
        """
        return self.test.questions.exclude(
            id__in=self.passed_questions.values_list('id', flat=True)
        ).first()

    def add_choice(self, question, choices):
        Question2UserTesting.objects.create(
            user_testing=self,
            question=question,
            state_right=question.is_right(choices)
        )

    def finish(self):
        self.state_done = True
        self.save()

    @classmethod
    def get(cls, user, test):
        user_testing, _ = cls.objects.get_or_create(user=user, test=test)
        return user_testing


class Question2UserTesting(models.Model):
    user_testing = models.ForeignKey(UserTesting)
    question = models.ForeignKey('Question')
    state_right = models.BooleanField(default=False)


class Test(models.Model):
    title = models.CharField(verbose_name='Название теста', max_length=255)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['title']

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('tests:test-detail', (self.pk,))


class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name='Тест', related_name='questions')
    text = models.TextField(verbose_name='Текст вопроса')
    sort = models.PositiveSmallIntegerField(verbose_name='Сортировка', default=500)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['sort']

    def __str__(self):
        return self.text

    def is_right(self, choices):
        if not isinstance(choices, models.QuerySet):
            choices = [choices]
        right_ids = set(self.choices.filter(state_right=True).values_list('id', flat=True))
        if right_ids == set([c.id for c in choices]):
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос', related_name='choices')
    text = models.CharField(verbose_name='Текст ответа', max_length=255)
    state_right = models.BooleanField(verbose_name='Правильный ответ', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text
