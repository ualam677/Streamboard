from django.urls import path
from .views import StreamboardCreateView, StreamboardDetailView

urlpatterns = [
    path('', StreamboardCreateView.as_view(), name='streamboard-create'),
    path('<uuid:id>/', StreamboardDetailView.as_view(), name='streamboard-detail'),

]
