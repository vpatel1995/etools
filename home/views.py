from django.shortcuts import render
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError

def home(request):
    return render(request, 'home/home.html')

def send_email_view(request):
    if request.method == 'POST':
        # AWS SES Configuration
        aws_access_key_id = 'AKIASD7G5KU2SHEC4B52'
        aws_secret_access_key = 'asxLtCguymmZJPTcX+kamBhPLCEhXkrFEbLVDhOS'
        aws_region = "us-east-2"  # Change as per your AWS SES configuration

        sender = "patelv2895@gmail.com"  # Your verified sender address
        recipient = "patelv2895@gmail.com"  # Your verified recipient address
        subject = "Amazon SES Test (SDK for Python)"
        body_text = ("Amazon SES Test\r\n"
                     "This email was sent with Amazon SES using the AWS SDK for Python (Boto).")
        body_html = """<html>
        <head></head>
        <body>
          <h1>Amazon SES Test (SDK for Python)</h1>
          <p>This email was sent with <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the AWS SDK for Python (Boto).</p>
        </body>
        </html>
        """

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
                        'Text': {
                            'Charset': "UTF-8",
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            return JsonResponse({'message': e.response['Error']['Message']}, status=500)
        else:
            return JsonResponse({'message': 'Email sent successfully! Message ID: {}'.format(response['MessageId'])}, status=200)

    return JsonResponse({'message': 'Invalid request'}, status=400)

