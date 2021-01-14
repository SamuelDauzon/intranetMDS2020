from django.urls import path

from calls import views, cbv

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
    path('call_edit_customer-<int:call_id>/', views.call_edit_customer, name="call_edit_customer"),
    path('new_call_customer/', views.new_call_customer, name="new_call_customer"),
    path('call_list_no_teammember/', views.call_list_no_teammember, name="call_list_no_teammember"),
    path('call_rating-<int:call_id>/', views.call_rating, name="call_rating"),
    path('bad_calls/', views.bad_calls, kwargs = {'call_id':3}, name="bad_calls"),
]
