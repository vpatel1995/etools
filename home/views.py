from django.shortcuts import render
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
import json
from django.conf import settings
import os


def get_template_content(request, template_id):
    try:
        # Construct the absolute file path
        file_path = os.path.join(settings.BASE_DIR, 'home', 'email_templates', f'template{template_id}.txt')
        
        with open(file_path, 'r') as file:
            content = file.read()
        return JsonResponse({'content': content})
    except FileNotFoundError:
        return JsonResponse({'error': 'Template not found'}, status=404)

def load_email_template(template_id):
    template_path = f"email_templates/template{template_id}.txt"
    with open(template_path, 'r') as file:
        return file.read()

def home(request):
    return render(request, 'home/home.html')

def send_email_view(request):
    if request.method == 'POST':
        # Parse the received JSON data
        data = json.loads(request.body)
        template_id = data.get('template_id')
        template_content = load_email_template(template_id)


        # AWS SES Configuration
        aws_access_key_id = 'AKIASD7G5KU2SHEC4B52'
        aws_secret_access_key = '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'
        aws_region = "us-east-2"

        sender = "patelv2895@gmail.com"
        recipient = "patelv2895@gmail.com"
        subject = data.get('subject')
        body_html = "<html><head></head><body>" + template_content + "</body></html>"

        # Create a new SES client
        client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # Try to send the email.
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [recipient],
                },
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
