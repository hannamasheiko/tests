from django.contrib import admin
from .models import Test, Question, Answer, Score, Comment

admin.site.register(Test)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Score)
