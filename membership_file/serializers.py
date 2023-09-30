from rest_framework import serializers

from .models import Member


# The MemberSerializer converts the Member model to a Python dictionary
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        depth = 0
