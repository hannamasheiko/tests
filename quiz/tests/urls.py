from django.conf.urls import url
from .views import add_test, tests_list, add_questions, test_detail, questions_list, add_answers, test_pass, \
    add_comment_to_test, test_result, test_filter

urlpatterns = [
    url(r'^test/$', add_test, name='test'),
    url(r'^$', tests_list),
    url(r'^test_filter/$',test_filter , name='test_filter'),
    url(r'^test/(?P<pk>[0-9]+)/$', test_detail, name='test_detail'),
    url(r'^test/(?P<test_id>[0-9]+)/add_questions/$', add_questions, name='add_questions'),
    url(r'^test/(?P<test_id>[0-9]+)/add_comment_to_test/$', add_comment_to_test, name='add_comment_to_test'),
    url(r'^test/(?P<test_id>[0-9]+)/questions_list/$', questions_list, name='questions_list'),
    url(r'^test/(?P<test_id>[0-9]+)/questions_list/(?P<question_id>[0-9]+)/add_answers/$', add_answers,
        name='add_answers'),
    url(r'^test/(?P<test_id>[0-9]+)/test_pass/$', test_pass, name='test_pass'),
    url(r'^test/(?P<test_id>[0-9]+)/test_pass/test_result/$', test_result, name='test_result'),

]
