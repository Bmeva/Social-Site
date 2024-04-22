from django.db import models
import uuid


 


class ShortUUIDField(models.CharField): 
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 32)
        kwargs.setdefault('default', self.generate_uuid)
        super().__init__(*args, **kwargs)

    def generate_uuid(self):
        # Generate UUID
        generated_uuid = uuid.uuid4().hex[:10]  # Take first 10 characters of UUID

        # Return truncated UUID
        return generated_uuid

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['default']
        return name, path, args, kwargs

