from rest_framework.serializers import ModelSerializer
from .mixins import DynamicFieldsMixin


class BaseModelSerializer(DynamicFieldsMixin, ModelSerializer):

    def _make_latest_field_getter(self, attrs):
        def get_latest_field(key: str):
            if key in attrs:
                return attrs[key]

            if self.instance and hasattr(self.instance, key):
                return getattr(self.instance, key)

            raise KeyError('cannot find field with key "{}"'.format(key))
        return get_latest_field
