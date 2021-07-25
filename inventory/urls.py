from django.urls import path, include

from inventory.views import *

namespace = 'inventory'

urlpatterns = [
    # Change Language helper view
    path('', BoardgameView.as_view(), name='home'),
    path('my_items/', include([
        path('', MemberItemsOverview.as_view(), name='member_items'),
        path('<int:ownership_id>/', include([
            path('take_ome/', MemberItemRemovalFormView.as_view(), name='member_take_home'),
            path('give_out/', MemberItemLoanFormView.as_view(), name='member_loan_out'),
            path('edit_note/', MemberOwnershipAlterView.as_view(), name='owner_link_edit'),
        ])),
    ])),
    path('committee/<int:group_id>/', include([
        path('items/', GroupItemsOverview.as_view(), name='committee_items'),
        path('<int:ownership_id>/', include([
            path('edit_note/', GroupItemLinkUpdateView.as_view(), name='owner_link_edit'),
        ])),
    ])),

]
