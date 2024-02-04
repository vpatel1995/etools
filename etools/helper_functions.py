from django.conf import settings
import os

def load_email_template(template_id):
    file_path = os.path.join(settings.BASE_DIR, 'home', 'email_templates', f'template{template_id}.txt')
    with open(file_path, 'r') as file:
        return file.read()