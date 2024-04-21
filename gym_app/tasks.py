from celery import shared_task
from .models import gymodel
from django.utils import timezone
from jdatetime import datetime as jdatetime


@shared_task
def update_users_status():
    gym_models = gymodel.objects.all()
    
    for gym_model in gym_models:
        if jdatetime.now().strftime('%Y-%m-%d') >= gym_model.end_date:
            gym_model.status = False
        else:
            gym_model.status = True
        gym_model.save(update_fields=['status'])

