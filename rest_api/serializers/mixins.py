from rest_framework import serializers
from rest_framework.request import Request
from typing import Literal, List


class DynamicFieldsMixin(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed during reading.

    Usage:
    >>> class MySerializer(BaseModelSerializer):
    >>>     class Meta:
    >>>         # ... other necessary configurations ...
    >>>         fields = ['aaa', 'bbb', 'ccc']
    >>>         default_include_fields = ['aaa', 'bbb'] # if not set, include all fields by default
    >>>         default_exclude_fields = ['aaa'] # has higher precedence than default_include_fields
    >>>         # The param above will include "bbb" by default, when "fields" query parameter does not presents in the request.
    >>>         # If the request contains "fields" query parameter, default_include_fields and default_exclude_fields will be ignored.
    """

    def __init__(self, *args, fields: List[str] | Literal['__all__'] | None = None, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        # if writing is happening, don't remove any fields
        if hasattr(self, 'initial_data'):
            return

        if fields is None:
            request = self.context.get('request', None)
            if request:
                fields = self._parse_request_fields(request)
        elif fields == '__all__':
            fields = self.fields.keys()

        include_fields: list = self.fields.keys()
        exclude_fields: list = []

        if fields is not None:
            include_fields = fields
        else:
            meta = self.Meta
            if hasattr(meta, 'default_include_fields'):
                include_fields = meta.default_include_fields
            elif hasattr(meta, 'default_exclude_fields'):
                exclude_fields = meta.default_exclude_fields

        unwanted_fields = (set(self.fields.keys())
                           .difference(include_fields)
                           .union(exclude_fields))

        for field_name in unwanted_fields:
            self.fields.pop(field_name, None)

    def _parse_request_fields(self, request: Request):
        fields_query = request.query_params.get('fields')
        if fields_query:
            return fields_query.split(',')
        else:
            return None
