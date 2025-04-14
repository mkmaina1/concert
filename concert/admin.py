from django.contrib import admin
from .models import News,Tickets,Merchandise,Album,Cart,CartItem
# Register your models here.

admin.site.register(News)
admin.site.register(Tickets)
admin.site.register(Merchandise)
admin.site.register(Album)
admin.site.register(Cart)
admin.site.register(CartItem)