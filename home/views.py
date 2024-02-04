from django.shortcuts import render
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
import json
from django.conf import settings
import os
from .models import EmailLog
from etools.helper_functions import load_email_template


def home(request):
    latest_email_log = EmailLog.objects.order_by('-sent_at').first()
    return render(request, 'home/home.html', {'latest_email_log': latest_email_log})
    #return render(request, os.path.join(settings.BASE_DIR, 'home', 'templates', 'home', 'home.html'))

def send_email_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        template_id = data.get('template_id')
        template_content = load_email_template(template_id)
        to_email = data.get('to_email')
        from_email = data.get('from_email')
        cc_email = data.get('cc_email')
        subject = data.get('subject')

        dynamic_fields = data.get('dynamic_fields', {})

        for key, value in dynamic_fields.items():
            placeholder = f"{{{{{key}}}}}"
            template_content = template_content.replace(placeholder, value)

        body_html = "<html><head></head><body>" + template_content + "</body></html>"

        aws_access_key_id = 'AKIASD7G5KU2SHEC4B52'
        aws_secret_access_key = 'asxLtCguymmZJPTcX+kamBhPLCEhXkrFEbLVDhOS'
        aws_region = "us-east-2"

        sender = from_email

        # Create a new SES client
        client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # Prepare the destination dictionary
        destination = {'ToAddresses': [to_email]}
        if cc_email:
            destination['CcAddresses'] = [cc_email]

        # Try to send the email.
        try:
            response = client.send_email(
                Destination=destination,
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': body_html,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            return JsonResponse({'message': e.response['Error']['Message']}, status=500)
        else:
            return JsonResponse({'message': 'Email sent successfully! Message ID: {}'.format(response['MessageId'])}, status=200)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def get_template_content(request, template_id):
    try:
        # Construct the absolute file path
        file_path = os.path.join(settings.BASE_DIR, 'home', 'email_templates', f'template{template_id}.txt')
        
        with open(file_path, 'r') as file:
            content = file.read()
        return JsonResponse({'content': content})
    except FileNotFoundError:
        return JsonResponse({'error': 'Template not found'}, status=404)