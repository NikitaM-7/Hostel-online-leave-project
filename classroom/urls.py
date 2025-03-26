from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([

    ], 'classroom'), namespace='students')),

    path('teachers/', include(([


    ], 'classroom'), namespace='teachers')),
     

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)