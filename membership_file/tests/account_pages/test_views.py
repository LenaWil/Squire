from django.test import TestCase
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView

from core.util import get_permission_objects_from_string
from user_interaction.account_pages.mixins import AccountTabsMixin
from utils.testing.view_test_utils import ViewValidityMixin

from membership_file.forms import MemberForm
from membership_file.models import Member
from membership_file.util import MembershipRequiredMixin
from membership_file.account_pages.views import MembershipDataView, MembershipChangeView


class MembershipDataViewTestCase(ViewValidityMixin, TestCase):
    """
    Tests the MembershipDataView class
    """
    fixtures = ['test_users', 'test_members.json']
    base_user_id = 100

    def test_class(self):
        self.assertTrue(issubclass(MembershipDataView, MembershipRequiredMixin))
        self.assertTrue(issubclass(MembershipDataView, AccountTabsMixin))
        self.assertEqual(MembershipDataView.model, Member)
        self.assertEqual(MembershipDataView.template_name, 'membership_file/membership_view.html')
        self.assertEqual(MembershipDataView.selected_tab_name, 'tab_membership')

    def test_permission_required(self):
        """ Tests that the agreed upon permissions are requiered """
        # No need to simulate, we can trust on PermissionRequiredMixin
        self.assertTrue(issubclass(MembershipDataView, PermissionRequiredMixin))
        self.assertEqual(MembershipDataView.permission_required, 'membership_file.can_view_membership_information_self')

    def test_successful_get(self):
        self.user.user_permissions.add(*list(get_permission_objects_from_string([MembershipDataView.permission_required])))
        response = self.client.get(reverse('account:membership:view'), data={})
        self.assertEqual(response.status_code, 200)


class MembershipChangeViewTestCase(ViewValidityMixin, TestCase):
    """
    Tests the MembershipDataView class
    """
    fixtures = ['test_users', 'test_members.json']
    base_user_id = 100

    def setUp(self):
        super(MembershipChangeViewTestCase, self).setUp()

        self.member = Member.objects.get(id=1)
        self.form_data = {
            "legal_name": self.member.legal_name,
            "first_name": self.member.first_name,
            "tussenvoegsel": self.member.tussenvoegsel,
            "last_name": self.member.last_name,
            "date_of_birth": self.member.date_of_birth,
            "email": self.member.email,
            "street": self.member.street,
            "house_number": self.member.house_number,
            "city": self.member.city,
            "country": self.member.country,
            "educational_institution": self.member.educational_institution,
            "student_number": self.member.student_number,
            "tue_card_number": self.member.tue_card_number,
        }

    def test_class(self):
        self.assertTrue(issubclass(MembershipChangeView, MembershipRequiredMixin))
        self.assertTrue(issubclass(MembershipChangeView, AccountTabsMixin))
        self.assertTrue(issubclass(MembershipChangeView, UpdateView))
        self.assertEqual(MembershipChangeView.form_class, MemberForm)
        self.assertEqual(MembershipChangeView.template_name, 'membership_file/membership_edit.html')
        self.assertEqual(MembershipChangeView.selected_tab_name, 'tab_membership')
        self.assertEqual(MembershipChangeView.success_url, reverse('account:membership:view'))

    def test_permission_required(self):
        """ Tests that the agreed upon permissions are required """
        # No need to simulate, we can trust on PermissionRequiredMixin
        self.assertTrue(issubclass(MembershipDataView, PermissionRequiredMixin))
        self.assertIn('membership_file.can_view_membership_information_self', MembershipChangeView.permission_required)
        self.assertIn('membership_file.can_change_membership_information_self', MembershipChangeView.permission_required)

    def test_successful_get(self):
        self.user.user_permissions.add(*list(get_permission_objects_from_string([MembershipDataView.permission_required])))
        response = self.client.get(reverse('account:membership:edit'), data={})
        self.assertEqual(response.status_code, 200)

    def test_valid_post(self):
        self.assertValidPostResponse(
            {
                **self.form_data,
                "house_number": 69,
            },
            url=reverse('account:membership:edit'),
            redirect_url=reverse('account:membership:view'),
            fetch_redirect_response=False
        )
        self.member.refresh_from_db()
        self.assertEqual(self.member.house_number, 69)
