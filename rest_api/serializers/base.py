from rest_framework.serializers import ModelSerializer
from .mixins import DynamicFieldsMixin


class BaseModelSerializer(DynamicFieldsMixin, ModelSerializer):

    def make_latest_field_getter(self, attrs):
        def get_latest_field(input_key: str, model_key: str = None, default=None, no_exception=False):
            if model_key is None:
                model_key = input_key

            if input_key in attrs:
                return attrs[input_key]

            if self.instance and hasattr(self.instance, model_key):
                return getattr(self.instance, model_key)

            if default is not None or no_exception:
                return default

            raise KeyError('cannot find field with key "{}"'.format(input_key))

        return get_latest_field
