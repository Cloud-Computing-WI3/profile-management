from django.contrib import admin
from accounts.models import Account, Category, Keyword

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Keyword)