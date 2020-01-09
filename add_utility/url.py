from django.urls import path
from .views import LoadWalletAPIView

app_name = 'add_utility'

urlpatterns = [
    path('utility/', LoadWalletAPIView.as_view()),
]
