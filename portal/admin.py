from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profession)


admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthdate', 'picture']


admin.site.register(LabourRequest)
admin.site.register(ClientRating)
admin.site.register(WorkerRating)
admin.site.register(LabourChat)
admin.site.register(ChatMessage)
admin.site.register(Administrator)
admin.site.register(Banning)
admin.site.register(LabourImage)
