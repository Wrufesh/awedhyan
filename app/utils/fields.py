# Base64FileField
import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.fields import SkipField


class Base64FieldMixin(object):
    def _decode(self, data):
        # print(data.get('dataURL'))
        # print(data.get('fileArray'))
        if data.get('fileArray'):
            data = data.get('dataURL')
        else:
            data = ''
        if isinstance(data, str) and data.startswith('data:'):
            # base64 encoded file - decode
            # print(data)
            format, datastr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(
                base64.b64decode(datastr),
                name='{}.{}'.format(uuid.uuid4(), ext)
            )

        elif isinstance(data, str) and data.startswith('http'):
            raise SkipField()

        return data

    def to_internal_value(self, data):
        data = self._decode(data)
        print(type(data))
        return super(Base64FieldMixin, self).to_internal_value(data)


class Base64ImageField(Base64FieldMixin, serializers.ImageField):
    pass


class Base64FileField(Base64FieldMixin, serializers.FileField):
    pass
