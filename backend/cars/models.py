from django.db import models
from users.models import User


class Seller(models.Model):
    PRO = 'pro'
    PARTICULIER = 'particulier'
    SELLER_TYPES = [(PRO, 'Professionnel'), (PARTICULIER, 'Particulier')]

    PLAN_FREE = 'free'
    PLAN_PREMIUM = 'premium'
    PLAN_CHOICES = [(PLAN_FREE, 'Gratuit'), (PLAN_PREMIUM, 'Premium')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPES, default=PRO)
    avatar = models.CharField(max_length=5)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)
    premium_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    FREE_CAR_LIMIT = 3

    @property
    def plan(self):
        from django.utils import timezone
        if self.is_premium and (self.premium_until is None or self.premium_until > timezone.now()):
            return self.PLAN_PREMIUM
        return self.PLAN_FREE

    @property
    def can_post(self):
        if self.plan == self.PLAN_PREMIUM:
            return True
        return self.cars.filter(is_available=True).count() < self.FREE_CAR_LIMIT

    class Meta:
        db_table = 'sellers'

    def __str__(self):
        return self.name


class Car(models.Model):
    FUEL_CHOICES = [
        ('Essence', 'Essence'),
        ('Diesel', 'Diesel'),
        ('Hybride', 'Hybride'),
        ('Électrique', 'Électrique'),
    ]
    TRANSMISSION_CHOICES = [
        ('Automatique', 'Automatique'),
        ('Manuelle', 'Manuelle'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField()
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    power = models.CharField(max_length=50)
    color = models.CharField(max_length=100)
    doors = models.IntegerField(default=4)
    seats = models.IntegerField(default=5)
    location = models.CharField(max_length=200)
    description = models.TextField()
    features = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    badge = models.CharField(max_length=50, blank=True)
    gradient = models.CharField(max_length=200, blank=True)
    accent_color = models.CharField(max_length=10, blank=True)
    image = models.URLField(max_length=500, blank=True)
    image_hero = models.URLField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cars'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.make} {self.model} {self.year}'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='appointments')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['date', 'time']

    def __str__(self):
        return f'{self.buyer} → {self.car} on {self.date}'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_images')
    image = models.FileField(upload_to='cars/')
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'car_images'
        ordering = ['-is_primary', 'order', 'created_at']

    def __str__(self):
        return f'Image #{self.order} — {self.car}'


class Report(models.Model):
    REASON_CHOICES = [
        ('fake',           'Annonce frauduleuse'),
        ('wrong_price',    'Prix trompeur'),
        ('not_responding', 'Vendeur ne répond pas'),
        ('not_serious',    'Vendeur pas sérieux'),
        ('already_sold',   'Véhicule déjà vendu'),
        ('harassment',     'Comportement inapproprié'),
        ('other',          'Autre raison'),
    ]
    STATUS_CHOICES = [
        ('pending',   'En attente'),
        ('resolved',  'Résolu'),
        ('dismissed', 'Rejeté'),
    ]
    ACTION_CHOICES = [
        ('',              'Aucune'),
        ('warn',          'Avertissement envoyé'),
        ('suspend_car',   'Annonce suspendue'),
        ('suspend_user',  'Compte suspendu'),
        ('ban_user',      'Compte banni'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_sent')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='reports_received')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True)
    admin_action = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']

    def __str__(self):
        return f'Report #{self.pk} — {self.reason}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        unique_together = ('user', 'car')
