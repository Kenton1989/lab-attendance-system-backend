from rest_framework import serializers
from rest_framework.request import Request
from typing import Literal, List


class DynamicFieldsMixin():
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed during reading. All writable fields
    will be kept during writing.

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

    def __init__(self,
                 *args,
                 fields: List[str] = None,  # or literal '__all__'
                 **kwargs):

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is None:
            request = self.context.get('request', None)
            if request:
                fields = self._parse_request_fields(request)
        elif fields == '__all__':
            fields = self.fields.keys()

        include_fields = None
        exclude_fields = None

        if fields is not None:
            include_fields = fields
        elif hasattr(self, 'Meta'):
            meta = self.Meta
            if hasattr(meta, 'default_include_fields'):
                include_fields = meta.default_include_fields
            if hasattr(meta, 'default_exclude_fields'):
                exclude_fields = meta.default_exclude_fields

        if include_fields is None and exclude_fields is None:
            return
        if include_fields is None:
            include_fields = self.fields.keys()
        if exclude_fields is None:
            exclude_fields = []

        unwanted_fields = (set(self.fields.keys())
                           .difference(include_fields)
                           .union(exclude_fields))

        for field_name in unwanted_fields:
            field = self.fields.get(field_name)
            if field.read_only:
                self.fields.pop(field_name)
            elif not field.write_only:
                field.write_only = True

    def _parse_request_fields(self, request: Request):
        fields_query = request.query_params.get('fields')
        if fields_query:
            return fields_query.split(',')
        else:
            return None
