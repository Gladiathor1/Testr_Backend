from django.urls import path
from . import views


urlpatterns = [
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('upload/tags/', views.upload_tags, name='upload_tags'),
    # path('delpapers/', views.delete_all),
    path('disciplines', views.DisciplineViewSet.as_view({'get': 'list', 'post': 'list'}), name="disciplines"),
    path('subjects', views.SubjectViewSet.as_view({'get': 'list', 'post': 'list'}), name="subjects"),
    path('papers', views.PaperViewSet.as_view({'get': 'list', 'post': 'list'}), name="papers"),
    path('questions', views.QuestionViewSet.as_view({'get': 'list', 'post': 'list'}), name="questions"),
    path('tags', views.TagViewSet.as_view({'get': 'list', 'post': 'list'}), name="tags"),

    # path('user', views.UserViewSet.as_view({'get': 'list'}), name="tags"),
]
