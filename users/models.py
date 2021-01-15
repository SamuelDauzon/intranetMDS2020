from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created       = models.DateTimeField(auto_now_add = True, verbose_name="Date de création")
    modified      = models.DateTimeField(auto_now = True, verbose_name="Date de modification")

    class Meta:
        abstract = True
        ordering = ("-created", )


class UserProfile(AbstractUser, BaseModel):

    USER_TYPE_CHOICES = (
        (1, 'teammember'),
        (2, 'client'),
        )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=None,
        blank=True,
        null=True,
        )

    # TODO : set CharField
    display_name = models.TextField(
        verbose_name="Nom d'affichage",
        default=None,
        blank=True,
        null=True,
        )

    newsletter_agreement = models.BooleanField(
        verbose_name = "Recevoir des newsletter",
        help_text = "Une par semaine maximum",
        default=False,
        db_index=True,
        )

    def is_teammember(self):
        return self.user_type == 1

    def is_customer(self):
        return self.user_type == 2

    def is_customer_or_teammember(self):
        return self.is_teammember() or self.is_customer()

    def __str__(self):
        if self.display_name :
            return self.display_name
        else:
            return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ("created", )


class TeamMember(BaseModel):

    teammember = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True,
        )

    support_level = models.PositiveSmallIntegerField(
        default=1,
        help_text = "0 expert, 5 débutant",
        )

    def __str__(self):
        return str(self.teammember)


class Customer(BaseModel):

    customer = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True,
        )

    credits = models.IntegerField(
        default=0,
        )

    def __str__(self):
        return str(self.customer)


