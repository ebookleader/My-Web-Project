from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 사이트에 보일 항목
    list_display = ('id','email','name','joined_at','last_login_at','is_superuser','is_active')
    # 클릭시 정보 수정으로 넘어가는 필드들
    list_display_links = ('id','email')
    # 상세정보에서 패스워드는 제외
    exclude = ('password',)

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")
    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    # 가장 최근에 가입한 사람부터 리스팅
    joined_at.admin_order_field = '-date_joined'
    # 필드명
    joined_at.short_description = 'joined ddate'
    last_login_at.admin_order_field = 'last_login_at'
    # 필드명
    last_login_at.short_description = 'last login'