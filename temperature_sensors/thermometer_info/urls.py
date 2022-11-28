from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views

urlpatterns = [
      path('', views.index),
      path('thermometers/location/<str:location>', views.thermometers_info_by_location),

      path('profile/', include('social_django.urls', namespace='social')),
      path('profile/logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},
           name='logout'),
      path('profile/secure/', views.secure, name='secure'),

      path('api/thermometers', views.ThermometersAPIView.as_view()),
      path('api/thermometers/<int:id>/', views.ThermometerAPIView.as_view()),
      path('api/thermometers/location/<str:location>', views.ThermometerLocationAPIView.as_view()),
      path('api/files/csv', views.FilesAPIView.as_view()),
]
