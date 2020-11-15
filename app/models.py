from django.db import models
from ckeditor.fields import RichTextField


class PrivacyPolicy(models.Model):
    privacy = RichTextField(verbose_name='Polityka prywatności')
    regulations = RichTextField(verbose_name='Regulamin strony')

    class Meta:
        verbose_name = 'Polityka prywatności i regulamin strony'
        verbose_name_plural = 'Polityka prywatności i regulamin strony'