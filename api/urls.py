from django.urls import path
from .views import( 
    SignupView,
    LoginView,
    QuestionListCreateView,
    QuestionRetrieveUpdateDeleteView,
    TestCaseListCreateView,
    TestCaseRetrieveUpdateDeleteView,
    SolutionCheckView,
                   
)
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteView.as_view(), name='question-detail'),
    path('testcases/', TestCaseListCreateView.as_view(), name='testcase-list'),
    path('testcases/<int:pk>/', TestCaseRetrieveUpdateDeleteView.as_view(), name='testcase-detail'),
    path('solution/check/', SolutionCheckView.as_view(), name='solution-check'),
]
