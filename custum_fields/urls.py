from django.urls import path
from .views import CountryCodeView, CountryView, StateView, CityView

urlpatterns = [
    path('country-codes/', CountryCodeView.as_view(), name='country_codes'),
    path('country-codes/<int:id>/', CountryCodeView.as_view(),
         name='country_code_detail'),
    path('countries/', CountryView.as_view(), name='countries'),
    path('countries/<int:id>/', CountryView.as_view(), name='country_detail'),
    path('states/', StateView.as_view(), name='states'),
    path('states/<int:id>/', StateView.as_view(), name='state_detail'),
    path('cities/', CityView.as_view(), name='cities'),
    path('cities/<int:id>/', CityView.as_view(), name='city_detail'),
]
