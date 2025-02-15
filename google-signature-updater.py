from string import Template
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import *
from google.auth.exceptions import *
import mysql.connector
import phonenumbers
import sys

# Database connection (Sanitized: Replace with actual credentials in config)
mydb = mysql.connector.connect(
  host="your_database_host",
  user="your_database_user",
  password="your_database_password",
  database="your_database_name"
)

def get_api_credentials(key_path):
    API_scopes = [
        'https://www.googleapis.com/auth/gmail.settings.basic',
        'https://www.googleapis.com/auth/gmail.settings.sharing'
    ]
    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=API_scopes)
    return credentials


def update_sig(full_name, job_title, telephone, us_mobile_number, username, sig_template, credentials, live=False):
    sig = sig_template
    if live:
        credentials_delegated = credentials.with_subject(username)
        gmail_service = build("gmail", "v1", credentials=credentials_delegated)
        addresses = gmail_service.users().settings().sendAs().list(userId='me', fields='sendAs(isPrimary,sendAsEmail)').execute().get('sendAs')

        address = None
        for address in addresses:
            if address.get('isPrimary'):
                break
        if address:
            rsp = gmail_service.users().settings().sendAs().patch(
                userId='me',
                sendAsEmail=address['sendAsEmail'],
                body={'signature': sig}
            ).execute()
            print(f"Signature changed for: {username}")
        else:
            print(f"Could not find primary address for: {username}")


def main():
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT users_cstm.emp_company_email_c, users.first_name, users.last_name, users_cstm.designation_c, users.phone_mobile, users_cstm.us_mobile_number_c "
        "FROM users INNER JOIN users_cstm ON users_cstm.id_c = users.id WHERE users.employee_status = 'Active' AND users.deleted = 0 AND users.id = %s",
        (sys.argv[1],)
    )
    myresult = mycursor.fetchall()

    credentials = get_api_credentials(key_path="your_json_key_path.json")  # Path to JSON key (replace)
    if not credentials:
        print("No credential file selected, stopping execution.")
        return

    for r in myresult:
        username = r[0]
        first_name = r[1] if r[1] else ''
        second_name = r[2] if r[2] else ''
        full_name = first_name + ' ' + second_name
        job_title = r[3] if r[3] else ''
        telephone = r[4] if r[4] else ''
        telephone = phonenumbers.format_number(phonenumbers.parse(telephone, 'IN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country = "India"
        us_mobile_number_c = r[5] if r[5] else ''
        
        sig_template = f"""
        <html><body><div><div dir="ltr" data-smartmail="gmail_signature">
        <p><strong>{full_name}</strong></p>
        <p><em>{job_title}</em></p>
        <p>Email: <a href="mailto:{username}">{username}</a></p>
        <p>Phone: {telephone}</p>
        </div></body></html>
        """

        retry_count = 0
        while retry_count < 3:
            try:
                update_sig(full_name, job_title, username, telephone, us_mobile_number_c, sig_template, credentials, live=True)
                break
            except (RefreshError, TransportError) as e:
                retry_count += 1
                print(f"Error encountered for {username}, retrying (attempt {retry_count}). Error: {e}")
                time.sleep(2)
                continue
            except Exception as e:
                raise
        else:
            print(f"Failed to update {username}")


if __name__ == '__main__':
    main()