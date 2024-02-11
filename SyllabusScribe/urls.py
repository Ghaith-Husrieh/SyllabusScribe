from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="SyllabusScribe APIs",
        default_version='v1.0.0-rc.1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/swagger/',
        schema_view.with_ui(renderer='swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path('api/', include('Base.urls')),
    path('api/large-language-model/', include('LargeLanguageModel.urls')),
    path('api/student-performance-model/', include('StudentPerformanceModel.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
