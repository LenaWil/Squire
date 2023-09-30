from django.urls import path, register_converter, reverse_lazy
from django.views.generic.base import RedirectView

from committees.committeecollective import registry
from committees.url_converters import AssociationgroupConverter
from committees.views import BoardOverview, CommitteeOverview, GuildOverview

register_converter(AssociationgroupConverter, "assoc_group")


app_name = "committees"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("committees:committees")), name="home"),
    path("committees/", CommitteeOverview.as_view(), name="committees"),
    path("guilds/", GuildOverview.as_view(), name="guilds"),
    path("boards/", BoardOverview.as_view(), name="boards"),
    path("<assoc_group:group_id>/", registry.get_urls(with_namespace=False)),
]
