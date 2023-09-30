from dynamic_preferences.users.forms import UserPreferenceForm

from mailcow_integration.squire_mailcow import SquireMailcowManager


class MemberMailPreferencesForm(UserPreferenceForm):
    """Form that allows changing member mail preferences"""

    def __init__(self, *args, mailcow_manager: SquireMailcowManager = None, **kwargs):
        self.mailcow_manager = mailcow_manager
        super().__init__(*args, **kwargs)

    def update_preferences(self, **kwargs):
        """Update mail preferences and invokes the SquireMailcowManager"""
        super().update_preferences(**kwargs)

        if self.has_changed():
            self.mailcow_manager.update_member_aliases()
