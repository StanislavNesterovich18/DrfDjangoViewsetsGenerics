import re

from rest_framework.exceptions import ValidationError


class UrlsValidator:

    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        url_pattern = re.compile(r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}')

        if self.field and isinstance(value, dict):
            tmp_val = value.get(self.field)
        else:
            tmp_val = value

        if not tmp_val:
            return

        elif not url_pattern.match(tmp_val):
            raise ValidationError('Введите корректный URL (должен начинаться с http:// или https://)')

        elif tmp_val.startswith('http'):
            print("Строка начинается с http")
            return tmp_val
