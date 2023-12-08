import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import datetime
import pytz
import csv

# Email credentials
my_email = "your_email@gmail.com"
password = "your_password"

# Email content
subject = "Your Subject"
body = "Your email body here."

# Timezone setup for EST
est = pytz.timezone('US/Eastern')

# Function to send email
def send_email(receiver_email):
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=receiver_email, msg=msg.as_string())
        print(f"Email sent successfully to {receiver_email}")
        record_sent_email(receiver_email)
    except Exception as e:
        print(f"An error occurred while sending to {receiver_email}: {e}")

# Function to record sent emails
def record_sent_email(email):
    with open('sent_emails.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([email])

# Function to check if current time is within the desired range
def is_time_in_range():
    # For testing, we return True always
    # current_time = datetime.datetime.now(est)
    # start_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    # end_time = current_time.replace(hour=17, minute=0, second=0, microsecond=0)
    # return start_time <= current_time <= end_time
    return True

# Function to check if email was already sent

def was_email_sent(email):
    try:
        with open('sent_emails.csv', mode='r', newline='', encoding='utf-8') as file:
            sent_emails = [row[0] for row in csv.reader(file)]
            return email in sent_emails
    except FileNotFoundError:
        return False  # File not found implies email was not sent


# Read email addresses from CSV
def read_emails_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row['email'] for row in reader]

# Main function to send emails
def main():
    email_list = read_emails_from_csv('path_to_your_csv_file.csv')
    emails_sent = 0

    for email in email_list:
        if emails_sent < 300 and not was_email_sent(email):
            send_email(email)
            emails_sent += 1
            time.sleep(100)  # Sleep for 100 seconds


if __name__ == "__main__":
    main()
