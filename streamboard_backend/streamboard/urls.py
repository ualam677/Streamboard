from django.urls import path
from .views import StreamboardCreateView, StreamboardDetailView, StreamboardListView,\
    StreamboardDetailUpdateView, RecentViewedStreamboardsView, LatestStreamboardView

urlpatterns = [
    path('', StreamboardCreateView.as_view(), name='streamboard-create'),
    path('list/', StreamboardListView.as_view(), name='streamboard-list'),
    path('<uuid:id>/', StreamboardDetailUpdateView.as_view(), name='streamboard-detail'),
    path('<uuid:id>/retrieve/', StreamboardDetailView.as_view(), name='streamboard-detail-retrieve'),
    path('recent-viewed/', RecentViewedStreamboardsView.as_view(), name='recent-viewed-streamboards'),
    path('latest/', LatestStreamboardView.as_view()),
]
