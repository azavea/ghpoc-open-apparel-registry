from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin

from api import models


class OarUserAdmin(UserAdmin):
    exclude = ('last_name', 'date_joined', 'first_name')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'is_staff', 'is_active',
                           'should_receive_newsletter',
                           'has_agreed_to_terms_of_service')}),
    )


class FacilityHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ['name', 'address', 'location']


admin.site.register(models.User, OarUserAdmin)
admin.site.register(models.Contributor)
admin.site.register(models.FacilityList)
admin.site.register(models.FacilityListItem)
admin.site.register(models.Facility, FacilityHistoryAdmin)
admin.site.register(models.FacilityMatch)
