from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
from flask_cors import CORS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

app = Flask(__name__)


# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)



aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = 'ap-south-1'

if not aws_access_key_id or not aws_secret_access_key:
    raise EnvironmentError("AWS credentials not found. Please set them as environment variables.")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

ec2 = session.resource('ec2')



# Load the account SID and Auth Token from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# Create a Twilio client
client = Client(account_sid, auth_token)

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        # Extract data from the POST request
        data = request.get_json()
        to_number = data['to']
        message_body = data['message']

        # Send the WhatsApp message
        message = client.messages.create(
            body=message_body,
            from_='whatsapp:+14155238886',  # Twilio Sandbox WhatsApp number
            to=f'whatsapp:{to_number}'
        )

        # Return a success response
        return jsonify({
            'status': 'success',
            'message_sid': message.sid,
            'message': 'Message sent successfully!'
        }), 200

    except Exception as e:
        # Return an error response
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        # Extract data from the POST request
        data = request.json
        to_number = data.get('to')
        message_body = data.get('body')

        # Validate input data
        if not to_number or not message_body:
            return jsonify({"error": "Please provide both 'to' and 'body' fields"}), 400

        # Send an SMS
        message = client.messages.create(
            body=message_body,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),  # Your Twilio phone number
            to=to_number
        )

        # Return a success response
        return jsonify({"message_sid": message.sid, "status": "Message sent successfully!"}), 200

    except Exception as e:
        # Return an error response
        return jsonify({"error": str(e)}), 500
    

@app.route('/make_call', methods=['POST'])
def make_call():
    try:
        # Extract data from the POST request
        data = request.json
        to_number = data.get('to')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio phone number

        # Validate input data
        if not to_number:
            return jsonify({"error": "Please provide the 'to' field"}), 400

        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url='http://demo.twilio.com/docs/voice.xml'  # This URL should point to TwiML
        )

        # Return a success response
        return jsonify({"call_sid": call.sid, "status": "Call initiated successfully!"}), 200

    except Exception as e:
        # Return an error response
        return jsonify({"error": str(e)}), 500


# Define the email sending function
def send_email(sender_email, receiver_email, subject, body, attachment_path=None):
    app_password = os.getenv("EMAIL_APP_PASSWORD")  # Fetch app password from environment variable

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, 'plain'))

    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(attachment_path)}",
                )
                message.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return False

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    data = request.form
    sender_email = data.get('sender_email')
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    body = data.get('body')
    attachment = request.files.get('attachment')

    if not sender_email or not receiver_email or not subject or not body:
        return jsonify({'error': 'Missing required fields'}), 400

    attachment_path = None
    if attachment:
        attachment_path = f"temp_{attachment.filename}"  # Save the attachment file temporarily
        try:
            attachment.save(attachment_path)
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save attachment'}), 500

    success = send_email(sender_email, receiver_email, subject, body, attachment_path)

    if attachment_path:
        try:
            os.remove(attachment_path)
        except Exception as e:
            print(f"Error removing file: {e}")

    if success:
        return jsonify({'message': 'Email sent successfully'}), 200
    else:
        return jsonify({'error': 'Failed to send email'}), 500
    


# Initialize the EC2 resource
ec2 = boto3.resource('ec2', region_name='ap-south-1')  # Replace with your region

@app.route("/launch-instance", methods=["POST"])
def launch_instance():
    try:
        data = request.json
        instance_type = data.get('instance_type', 't2.micro')
        ami_id = data.get('ami_id', 'ami-0e53db6fd757e38c7')

        instances = ec2.create_instances(
            InstanceType=instance_type,
            ImageId=ami_id,
            MaxCount=1,
            MinCount=1
        )

        instance_ids = [instance.id for instance in instances]
        return jsonify({"message": "Instance launched", "instance_ids": instance_ids})
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return jsonify({"error": f'Credentials error: {str(e)}'}), 500
    except ClientError as e:
        return jsonify({"error": f'Client error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stop-instance", methods=["POST"])
def stop_instance():
    try:
        data = request.json
        instance_id = data.get('instance_id')

        instance = ec2.Instance(instance_id)
        instance.stop()

        return jsonify({"message": f"Instance {instance_id} stopped"})
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return jsonify({"error": f'Credentials error: {str(e)}'}), 500
    except ClientError as e:
        return jsonify({"error": f'Client error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/terminate-instance", methods=["POST"])
def terminate_instance():
    try:
        data = request.json
        instance_id = data.get('instance_id')

        instance = ec2.Instance(instance_id)
        instance.terminate()

        return jsonify({"message": f"Instance {instance_id} terminated"})
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return jsonify({"error": f'Credentials error: {str(e)}'}), 500
    except ClientError as e:
        return jsonify({"error": f'Client error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list-instances")
def list_instances():
    try:
        instances = ec2.instances.all()
        instance_list = []

        for instance in instances:
            instance_list.append({
                "instance_id": instance.id,
                "instance_type": instance.instance_type,
                "state": instance.state['Name'],
                "launch_time": instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify({"instances": instance_list})
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return jsonify({"error": f'Credentials error: {str(e)}'}), 500
    except ClientError as e:
        return jsonify({"error": f'Client error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
