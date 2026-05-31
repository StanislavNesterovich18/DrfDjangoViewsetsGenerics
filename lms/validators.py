import re

from rest_framework.exceptions import ValidationError

def urls_validator(url):
    url_pattern = re.compile(r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}')
    if not url_pattern.match(url):
        raise ValidationError('Введите корректный URL (должен начинаться с http:// или https://)')
    return url
