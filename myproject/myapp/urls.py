from django.urls import path
from .views import ContractDetailsView

urlpatterns = [
    path('contract-details/', ContractDetailsView.as_view(), name='contract-details'),
]
