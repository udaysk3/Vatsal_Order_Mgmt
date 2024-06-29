from django.contrib import admin
from .models import Item, Topup, ChatNote
# Register your models here.
admin.site.register(Item)
admin.site.register(Topup)
admin.site.register(ChatNote)