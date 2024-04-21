from django.contrib import admin
from .models import gymodel ,user
from django.utils import timezone
from django.contrib.auth.models import User , Group


class gymodelAdmin(admin.ModelAdmin):
   
    list_display = ["name","start_date","end_date","status"]  
    list_filter  = ("status","start_date",) 
    search_fields = ["name","phone",]
    ordering = ('end_date',)

    def time (self,request):
          qs = super().get_queryset(request)

          Start_date = timezone.now() - timezone.timedelta(days=30)
          return qs.filter(start_date__gts=Start_date)


class userAdmin (admin.ModelAdmin):
        list_display = ["name","status",]  
        search_fields = ["user",]
        list_filter  = ("status",) 
        ordering = ('status',)


      

admin.site.register(gymodel,gymodelAdmin)
admin.site.register(user,userAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)


