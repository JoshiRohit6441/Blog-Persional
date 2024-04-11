from django.db import models


class CountryCode(models.Model):
    country_name = models.CharField(max_length=250)
    country_code = models.IntegerField()
    country_flag = models.ImageField(upload_to="country_flag_contact")

    def __str__(self):
        return f"{self.country_name} ({self.country_code})"


class CountryModel(models.Model):
    country_name = models.CharField(max_length=250)
    flags = models.ImageField(upload_to="country_flags")

    def __str__(self):
        return self.country_name


class StateModal(models.Model):
    state_name = models.CharField(max_length=250)
    country = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.state_name}, {self.country.country_name}"


class CityModal(models.Model):
    city = models.CharField(max_length=250)
    state = models.ForeignKey(
        StateModal, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}, {self.state.state_name}, {self.country.country_name}"
