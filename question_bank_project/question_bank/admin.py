from django.contrib import admin
from .models import *

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Option)
#admin.site.register(User)

# @admin.register(Subject)
# class UserAdmin1(admin.ModelAdmin):
#     list_display=('id','name')


# @admin.register(Question)
# class UserAdmin2(admin.ModelAdmin):
#     list_display=('id','qus')

# @admin.register(Option)
# class UserAdmin3(admin.ModelAdmin):
#     list_display=('id','text','qus','is_correct')

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=('id','name','email','password')
