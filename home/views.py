from django.shortcuts import render
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
import json

def home(request):
    return render(request, 'home/home.html')

def send_email_view(request):
    if request.method == 'POST':
        # Parse the received JSON data
        data = json.loads(request.body)
        template_id = data.get('template_id')
        template_content = data.get('template_content')

        # AWS SES Configuration
        aws_access_key_id = 'AKIASD7G5KU2SHEC4B52'
        aws_secret_access_key = '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'
        aws_region = "us-east-2"

        sender = "patelv2895@gmail.com"
        recipient = "patelv2895@gmail.com"
        subject = "Email Template " + template_id
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
