from django.urls import path

from .views import upgrade_me, BaseUpdateView


urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    path('profile/edit/', BaseUpdateView.as_view(template_name='edit.html'),
         name='profile_edit'),

]