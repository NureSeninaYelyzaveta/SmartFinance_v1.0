from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Emotion(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Дохід'),
        ('expense', 'Витрата'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    emotion = models.ForeignKey(Emotion, on_delete=models.SET_NULL, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"

    def get_type_display_name(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return int((self.saved_amount / self.target_amount) * 100)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    LANGUAGE_CHOICES = [
        ('uk', 'Українська'),
        ('en', 'English'),
    ]
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='uk')

    THEME_CHOICES = [
        ('light', 'Світла'),
        ('dark', 'Темна'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    CURRENCY_CHOICES = [
        ('UAH', '₴'),
        ('USD', '$'),
        ('EUR', '€'),
        ('PLN', 'zł'),
    ]
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='UAH')

    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)