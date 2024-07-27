from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='Oluşturulma'
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        help_text='Oluşturan',
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_cby',
        editable=False
    )

    modified_on = models.DateTimeField(
        auto_now=True,
        help_text='Güncelleme'
    )
    modified_by = models.ForeignKey(
        User,
        null=True,
        help_text='Güncelleyen',
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_mby',
        editable=False
    )
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.save()


class Device(BaseModel):
    name = models.CharField(max_length=200, unique=True,
                            blank=False, null=False, db_index=True)

    class Meta:
        db_table = 'device'

    def latest_location(self):
        return self.location_set.order_by('-created_on').first()


class Location(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'location'
