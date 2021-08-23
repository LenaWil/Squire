from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, IntegerField
from django.forms.widgets import HiddenInput

from committees.models import GroupExternalUrl, AssociationGroup


class DeleteGroupExternalUrlForm(Form):

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        super(DeleteGroupExternalUrlForm, self).__init__(*args, **kwargs)

    def clean(self):
        raise ValidationError("Well well well", code='well')

    def delete(self):
        self.instance.delete()


class AddOrUpdateExternalUrlForm(ModelForm):
    id = IntegerField(min_value=0, required=False, widget=HiddenInput)

    class Meta:
        model = GroupExternalUrl
        exclude = ['association_group',]

    def __init__(self, *args, association_group=None, **kwargs):
        assert association_group is not None
        self.association_group = association_group
        super(AddOrUpdateExternalUrlForm, self).__init__(*args, **kwargs)

    def clean_id(self):
        try:
            self.instance = GroupExternalUrl.objects.get(id=self.cleaned_data['id'])
        except GroupExternalUrl.DoesNotExist:
            # Connect the association group to the new model instance
            self.instance.association_group = self.association_group
            return None
        if self.instance not in self.association_group.shortcut_set.all():
            raise ValidationError(f"Shortcut was not part of {self.association_group}", code='unconnected')

        return self.cleaned_data['id']

    def save(self, commit=True):
        created = self.instance.id is None
        super(AddOrUpdateExternalUrlForm, self).save(commit=commit)
        return self.instance, created


