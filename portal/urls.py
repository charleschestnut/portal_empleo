import portal.views as views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    path('', views.search_list, name='search_list'),

    path('populate', views.populate, name='populate'),

    path('profile/<int:id>/', views.profile_display, name='profile_display'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),

    path('labour-request/request/<int:id>/', views.labour_request, name='labour_request'),
    path('labour-request/pending/', views.labour_list_pending, name='labour_list_pending'),
    path('labour-request/in-process/', views.labour_list_in_process, name='labour_list_in_process'),
    path('labour-request/finished/', views.labour_list_finished, name='labour_list_finished'),
    path('labour-request/sent/', views.labour_list_sent, name='labour_list_sent'),
    path('labour-request/accept/<int:id>', views.labour_accept, name='labour_accept'),
    path('labour-request/reject/<int:id>', views.labour_reject, name='labour_reject'),
    path('labour-request/cancel/<int:id>', views.labour_cancel, name='labour_cancel'),
    path('labour-request/worker-finish/<int:id>', views.labour_worker_finish, name='labour_worker_finish'),
    path('labour-request/total-finish/<int:id>', views.labour_total_finish, name='labour_total_finish'),


    path('labour-request/worker-rating/<int:id>', views.worker_rating_create, name='worker_rating_create'),
    path('labour-request/client-rating/<int:id>', views.client_rating_create, name='client_rating_create'),


    path('rating/list/<str:type>/<int:id>', views.rating_list, name='rating_list'),


    path('labour_chat/<int:id>', views.chat_display, name='chat_display'),
    path('labour_chat/list', views.chat_list, name='chat_list'),
]

#    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#
#    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
#    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),#
#
#    # reset password urls
#    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),