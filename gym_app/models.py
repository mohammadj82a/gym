from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from jdatetime import datetime as jdatetime
from datetime import datetime, timedelta
from django.contrib.postgres.fields import JSONField



# class WeightHistory(models.Model):
#     gymodel = models.ForeignKey('gymodel', on_delete=models.CASCADE, related_name='weight_history')
#     weight = models.IntegerField()
#     date = models.DateField(default=timezone.now)

#     class Meta:
#         ordering = ['-date']

class gymodel(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField(default=10)
    height = models.FloatField(default=150)
    weight = models.FloatField(default=50)
    phone = models.CharField(max_length=11, blank=True)
    start_date = models.CharField(max_length=10, default=jdatetime.now().strftime('%Y-%m-%d'))
    end_date = models.CharField(max_length=10, default=(jdatetime.now() + timezone.timedelta(days=30)).strftime('%Y-%m-%d'))
    renewal = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date'] 

    def __str__(self):
        return self.name
    
    @property
    def bmi(self):
        height_in_meters = self.height / 100 
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2)

@receiver(post_save, sender=gymodel)
def update_status(sender, instance, created, **kwargs):
        if jdatetime.now().strftime('%Y-%m-%d') >= instance.end_date:
            instance.status = False
        else:
            instance.status = True

    
@receiver(post_save, sender=gymodel)
def update_dates_on_renewal(sender, instance, **kwargs):
    if instance.renewal:
        instance.start_date = jdatetime.now().strftime('%Y-%m-%d')
        instance.end_date = (jdatetime.now() + timezone.timedelta(days=30)).strftime('%Y-%m-%d') 
        instance.status = True   
        instance.renewal = False
        gymodel.objects.filter(pk=instance.pk).update(start_date=instance.start_date, end_date=instance.end_date,status=True,renewal=False)
        instance.save()  



class user(models.Model):
    user = models.ForeignKey(gymodel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name


@receiver(post_save, sender=gymodel)
def update_user(sender, instance, **kwargs):
    try:
        user_instance = user.objects.get(user=instance)
    except user.DoesNotExist:
        user_instance = user.objects.create(user=instance)
    
    user_instance.name = instance.name
    user_instance.description = "Updated description"
    user_instance.status = instance.status
    user_instance.save()
