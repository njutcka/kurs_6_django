from django.contrib import admin

from main.models import Client, Mailing, Msg, Logfile

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Msg)
admin.site.register(Logfile)
