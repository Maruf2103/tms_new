# debug_templates.py
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_tms_django.settings')
django.setup()

from django.template.loader import get_template

try:
    template = get_template('custom_admin/dashboard.html')
    print('SUCCESS: Template found and loaded!')
    print(f'Template path: {template.origin.name}')
except Exception as e:
    print(f'ERROR: {e}')
    print('Template directories searched:')
    for loader in settings.TEMPLATES[0]['DIRS']:
        print(f'  - {loader}')
