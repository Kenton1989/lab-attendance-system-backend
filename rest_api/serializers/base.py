from rest_framework.serializers import ModelSerializer
from .mixins import DynamicFieldsMixin


class BaseModelSerializer(DynamicFieldsMixin, ModelSerializer):

    def make_latest_field_getter(self, attrs):
        def get_latest_field(deserialized_key: str, default=None, no_exception=False):
            if deserialized_key in attrs:
                return attrs[deserialized_key]

            if self.instance and hasattr(self.instance, deserialized_key):
                return getattr(self.instance, deserialized_key)

            if default is not None or no_exception:
                return default

            raise KeyError(
                'cannot find field with key "{}"'.format(deserialized_key))

        return get_latest_field
