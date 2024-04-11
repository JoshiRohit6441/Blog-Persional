from django.contrib import admin
from .models import CountryCode, CityModal, CountryModel, StateModal
from django.utils.html import format_html


class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_code', 'country_name', 'display_flag')

    def display_flag(self, obj):
        return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.country_flag.url)


admin.site.register(CountryCode, CountryCodeAdmin)


class CustumCityAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'state', 'country']


admin.site.register(CityModal, CustumCityAdmin)


class CustumStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_state']

    def get_state(self, obj):
        return obj.state_name

    get_state.short_description = 'State'


admin.site.register(StateModal, CustumStateAdmin)


class CustumCountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_country', "get_flags"]

    def get_country(self, obj):
        return obj.country_name

    get_country.short_description = 'Country'

    def get_flags(self, obj):
        return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.flags.url)


admin.site.register(CountryModel, CustumCountryAdmin)
