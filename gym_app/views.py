from .models import gymodel
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.views.generic import DeleteView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import GymodelForm 
from django.shortcuts import render
from jdatetime import datetime as jdatetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def main(request, pk = None):
    status_filter = request.GET.get('status_filter')

    if status_filter == 'true':
        posts = gymodel.objects.filter(status=True)
    elif status_filter == 'false':
        posts = gymodel.objects.filter(status=False)
    elif status_filter == 'today':
        today = jdatetime.now().strftime('%Y-%m-%d')
        posts = gymodel.objects.filter(start_date=today)
    elif status_filter == 'last_week':
        week = jdatetime.now() - timedelta(days=7)
        posts = gymodel.objects.filter(start_date__gte=week)
    elif status_filter == 'last_month':
        month = jdatetime.now() - timedelta(days=30)
        posts = gymodel.objects.filter(start_date__gte=month)
    elif status_filter == 'last_year':
        year = jdatetime.now() - timedelta(days=365)
        posts = gymodel.objects.filter(start_date__gte=year)
    else:
        posts = gymodel.objects.all()

    for post in posts:
        post.start_date = jdatetime.strptime(str(post.start_date), '%Y-%m-%d').strftime('%Y/%m/%d')
        post.end_date = jdatetime.strptime(str(post.end_date), '%Y-%m-%d').strftime('%Y/%m/%d')

    context = {'posts': posts}
    total_models = gymodel.objects.count()
    month = jdatetime.now() - timedelta(days=30)
    time_last_month = gymodel.objects.filter(start_date__gte=month).count()
    total_models_true = gymodel.objects.filter(status=True).count()
    total_models_false = gymodel.objects.filter(status=False).count()


    models = gymodel.objects.all()
    
    for model in models:
        if jdatetime.now().strftime('%Y-%m-%d') >= model.end_date:
            model.status = False
        else:
            model.status = True
        model.save()

    return render(request, 'main.html', {'posts': posts, 'total_models': total_models ,'total_models_true': total_models_true ,'total_models_false':total_models_false,'time_last_month':time_last_month})

   
@login_required
def gymodel_create(request , pk = None):
    form = GymodelForm(request.POST or None)
    if request.method == 'POST':
        form = GymodelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main.html')
    return render(request, 'singup.html', {'form': form})

@login_required
def gymodel_edit(request, pk=None):
    posts = gymodel.objects.all()
    instance = gymodel.objects.get(pk=pk)
    form = GymodelForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        form = GymodelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('main.html', pk=pk)

    context = {'form': form, 'posts': posts}  
    return render(request, 'gymodel_form.html', context)  

from .models import update_dates_on_renewal , update_status

@login_required
def gymodel_detail(request, pk=None):
    instance = gymodel.objects.get(pk=pk)
    all_models = gymodel.objects.all()

    
    for model in all_models:
        if jdatetime.now().strftime('%Y-%m-%d') >= model.end_date:
            model.status = False
        else:
            model.status = True
        model.save()

    form = GymodelForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        form = GymodelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('gymodel_detail.html', pk=pk)

    return render(request, 'gymodel_detail.html', {'instance': instance, 'form': form})






@login_required
def status(request , pk = None):
    status_filter = request.GET.get('status_filter')

    if status_filter == 'true':
        posts = gymodel.objects.filter(status=True)
    elif status_filter == 'false':
        posts = gymodel.objects.filter(status=False)
    elif status_filter == 'today':
        today = jdatetime.now().strftime('%Y-%m-%d')
        posts = gymodel.objects.filter(start_date=today)
    elif status_filter == 'last_week':
        start_date = jdatetime.now() - timedelta(days=7)
        posts = gymodel.objects.filter(start_date__gte=start_date)
    elif status_filter == 'last_month':
        start_date = jdatetime.now() - timedelta(days=30)
        posts = gymodel.objects.filter(start_date__gte=start_date)
    elif status_filter == 'last_year':
        start_date = jdatetime.now() - timedelta(days=365)
        posts = gymodel.objects.filter(start_date__gte=start_date)
    else:
        posts = gymodel.objects.all()
        
    for post in posts:
        post.start_date = jdatetime.strptime(str(post.start_date), '%Y-%m-%d').strftime('%Y/%m/%d')
        post.end_date = jdatetime.strptime(str(post.end_date), '%Y-%m-%d').strftime('%Y/%m/%d')


    context = {'posts': posts}
    return render(request, 'status.html', context)

class gymodelDeleteView(DeleteView,LoginRequiredMixin):
    model = gymodel
    success_url =  reverse_lazy('main')

@login_required
def search_view(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
        if search_text:
            results = gymodel.objects.filter(name__icontains=search_text)
            return render(request, 'search_results.html', {'results': results})
    return render(request, 'search_results.html', {'results': None})
   

@login_required
def search_results(request):
    if 'search_text' in request.GET:
        search_text = request.GET['search_text']
        if search_text:
            results = gymodel.objects.filter(name__icontains=search_text)
            return render(request, 'search_results.html', {'results': results})
    return render(request, 'search_results.html')


def reload_models(request):
    models = gymodel.objects.all()
    
    for model in models:
        if jdatetime.now().strftime('%Y-%m-%d') >= model.end_date:
            model.status = True
        else:
            model.status = False
        model.save()

    return JsonResponse({'status': 'success'})

def home(request):
    return render(request, 'main.html')


