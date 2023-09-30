from django import template

register = template.Library()

##################################################################################
# Template Filter that obtains the labels for selected instances of a multichoice-field
# @since 02 JAN 2021
##################################################################################


@register.filter
def selected_m2m_labels(form, fieldname):
    return [label for value, label in form.fields[fieldname].choices if value in form[fieldname].value()]
