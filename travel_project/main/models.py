# main/models.py
from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    CONTINENT_CHOICES = [
        ("Europe", "Европа"),
        ("Asia", "Азия"),
        ("North America", "Северная Америка"),
        ("South America", "Южная Америка"),
        ("Africa", "Африка"),
        ("Oceania", "Океания"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="URL")
    continent = models.CharField(max_length=50, choices=CONTINENT_CHOICES, verbose_name="Континент")
    description = models.TextField(verbose_name="Описание", blank=True)
    population_mil = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Население (млн)", null=True, blank=True)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Площадь (км²)", null=True, blank=True)
    gdp_usd = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="ВВП ($)", null=True, blank=True)
    image = models.ImageField(upload_to="destinations/", verbose_name="Изображение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.continent})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def formatted_population(self):
        return f"{self.population_mil} млн" if self.population_mil else "—"

    @property
    def formatted_area(self):
        return f"{self.area_km2:,} км²".replace(",", " ") if self.area_km2 else "—"

    @property
    def formatted_gdp(self):
        return f"${self.gdp_usd:,}".replace(",", " ") if self.gdp_usd else "—"


class Place(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="places", verbose_name="Страна/направление")
    title = models.CharField(max_length=200, verbose_name="Название места")
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="places/", verbose_name="Фото")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f"{self.title} ({self.destination.title})"


from django.db import models

class WeeklyOffer(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена (USD)", max_digits=10, decimal_places=2)
    bookings = models.PositiveIntegerField("Количество броней", default=0)
    days = models.PositiveIntegerField("Дней тура", default=1)
    includes_flight = models.BooleanField("Включён перелёт", default=True)
    includes_hotel = models.BooleanField("Включён отель", default=True)
    includes_excursions = models.BooleanField("Включены экскурсии", default=True)
    image = models.ImageField("Изображение", upload_to="offers/", blank=True, null=True)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='weekly_offers')

    def __str__(self):
        return f"{self.title} для {self.destination.title}"
