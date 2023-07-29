"""testr_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from question import views as qviews
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Question App
router.register(r'disciplines', qviews.DisciplineViewSet)
router.register(r'subjects', qviews.SubjectViewSet)

router.register(r'papers', qviews.PaperViewSet, basename='papers')
router.register(r'tags', qviews.TagViewSet)

router.register(r'questions', qviews.QuestionViewSet)
router.register(r'myquestions', qviews.myQuestionViewSet)
router.register(r'images', qviews.ImageViewSet)
router.register(r'review', qviews.VerfierViewSet)



schema_view = get_schema_view(
    openapi.Info(
        title="TESTR APP API",
        default_version='v1',
        description="API endpoints for using TESTR services",
        terms_of_service="https://testr.pk/policies/terms/",
        contact=openapi.Contact(email="contact@testr.pk"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger
    path('testr-api/swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('testr-api/api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('testr-api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('testr-api/rest', include(router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),

    # Admin
    path('testr-api/admin/', admin.site.urls),

    # Authentication
    path('testr-api/auth/', include('authentication.urls')),

    # Question Engine
    path('testr-api/engine2/', include('question.urls')),

    path('testr-api/engine/', include(router.urls)),
    # social Engine
    path('testr-api/social/', include('social_auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)