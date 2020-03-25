from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'date_joined', 'last_login', 'is_superuser', 'is_active')
    list_display_links = ('email', 'id', )
    exclude = ('password', )

    #
    # def joined_at(self, obj):
    #     return obj.date_joined.strftime("%Y-%m-%d")
    #
    # def last_login_at(self, obj):
    #     return obj.last_login.strftime("%Y-%m-%d %H:%m")
    #
    # joined_at.admin_order_field = '-date_joined'
    # joined_at.short_description = 'joined date'
    # last_login_at.short_description = 'last login'