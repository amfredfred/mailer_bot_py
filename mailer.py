import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from string import Template

def send_email(subject, body, to_email):
    smtp_server = 'your_smtp_server'
    smtp_port = 587
    smtp_username = 'your_smtp_username'
    smtp_password = 'your_smtp_password'

    from_email = 'your_email@example.com'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = Header(subject, 'utf-8')

    # Use the string.Template to substitute placeholders in the email body
    body_template = Template(body)
    body_content = body_template.substitute(name='John Doe')  # Example: Replace 'name' placeholder

    # Set the email body as HTML with inline styles
    msg.attach(MIMEText(body_content, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Read email addresses from a CSV file
with open('email_addresses.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader, None)  # Skip header row if present

    # Create CSV files for sent and failed emails
    sent_filename = 'sent-emails.csv'
    failed_filename = 'failed-emails.csv'
    if not header:
        write_to_csv(sent_filename, ['Email'])
        write_to_csv(failed_filename, ['Email'])

    for row in reader:
        email_address = row[0]
        subject = 'Your Subject'

        # Example HTML-styled template with inline styles
        body_template = """
            <html>
                <head>
                    <style>
                        body {
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f4;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #fff;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                        }
                        h1 {
                            color: #333;
                        }
                        p {
                            color: #555;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Hello, $name!</h1>
                        <p>This is your personalized HTML-styled email template.</p>
                    </div>
                </body>
            </html>
        """

        success = send_email(subject, body_template, email_address)

        if success:
            write_to_csv(sent_filename, [email_address])
        else:
            write_to_csv(failed_filename, [email_address])

        with open('email_addresses.csv', 'r') as infile:
            lines = infile.readlines()
        with open('email_addresses.csv', 'w') as outfile:
            for line in lines:
                if line.strip() != email_address:
                    outfile.write(line)

        time.sleep(2)  # Introduce a 2-second delay

print("Bulk email sending and processing completed.")