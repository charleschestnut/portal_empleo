from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('done/', views.payment_done, name='done'),
    path('successful/<int:id>', views.payment_sucessful, name='payment_successful'),
    path('cancelled/', views.payment_cancelled, name='cancelled'),
    path('process/<int:id>', views.payment_process, name='payment_process'),
]