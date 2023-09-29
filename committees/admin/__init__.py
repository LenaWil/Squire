from django.contrib import admin

from committees.models import AssociationGroup, GroupExternalUrl

from .models import AssociationGroupPanelControl
from .options import AssociationGroupAdmin, GroupExternalURLAdmin, GroupPanelAccessAdmin

admin.site.register(AssociationGroup, AssociationGroupAdmin)
admin.site.register(GroupExternalUrl, GroupExternalURLAdmin)
admin.site.register(AssociationGroupPanelControl, GroupPanelAccessAdmin)
