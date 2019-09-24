from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_module

import_module('user', package='quiz')

from user.models import CustomUser


class Test(models.Model):
    author = models.ForeignKey(to=CustomUser,
                               on_delete=models.CASCADE,
                               related_name='tests')
    title = models.CharField(max_length=200)
    test_text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_date',)


class Comment(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    comment_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ('-created_date',)


class Question(models.Model):
    test = models.ForeignKey(to=Test,
                             on_delete=models.CASCADE,
                             related_name='questions')
    question_text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def get_answers_variant(self):
        return Answer.objects.filter(question=self.id)


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE,
                                 related_name='answers')
    accepted = models.BooleanField(default=False)


class Score(models.Model):
    user = models.ForeignKey(to=CustomUser,
                             on_delete=models.CASCADE,
                             related_name='scores')
    test = models.ForeignKey(to=Test,
                             on_delete=models.CASCADE,
                             related_name='scores')
    count_right = models.IntegerField()
    count_wrong = models.IntegerField()
    percentage_correct_answers = models.FloatField()
