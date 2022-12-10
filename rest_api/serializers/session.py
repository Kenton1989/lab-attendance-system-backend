from rest_framework import serializers
from rest_api.models import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'group', 'lab', 'room_no',
                  'start_datetime', 'end_datetime',
                  'is_compulsory', 'allow_late_check_in', 'check_in_deadline',
                  'is_active']
