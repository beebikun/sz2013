from django.contrib import admin
from sz.core.models import *

admin.site.register(Races)
admin.site.register(Gender)


class UserAdmin(admin.ModelAdmin):
    list_filter = ['date_joined',]
admin.site.register(User, UserAdmin)

admin.site.register(Face)
admin.site.register(Category)
admin.site.register(MessagePreview)