from django.urls import path

from calls import views
from calls import cbv

app_name = 'calls'

urlpatterns = [
    path('new_call/', views.new_call, name="new_call"),
    path('call_list/', views.call_list, name="call_list"),
    path('call_edit-<int:call_id>/', views.call_edit, name="call_edit"),
    path(
        'call_delete-<int:pk>/',
        cbv.CallDeleteView.as_view(),
        name="call_delete"
        ),
]