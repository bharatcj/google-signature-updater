### Google Signature Updater

A Python script to update email signatures in Google Workspace automatically.

## Features
- Fetches user data from a MySQL database.
- Updates Gmail signatures using the Google API.
- Supports a retry mechanism for error handling.
- Uses **Google OAuth 2.0 Service Account** for authentication.

---

## Installation

### **1. Install Python and Required Libraries**
Ensure you have Python installed. If not, download and install it from [Python.org](https://www.python.org/downloads/).

Then, install the required dependencies:

```sh
pip3 install google-api-python-client phonenumbers mysql-connector-python
```

---

### **2. Configure Google Cloud API**
To allow the script to modify Gmail signatures, follow these steps:

1. **Go to Google Cloud Console**: [Google Cloud Console](https://console.cloud.google.com/)
2. **Create a New Project**:
   - Name it **User Signature Standardization**.
3. **Enable the Gmail API**:
   - Go to **APIs & Services > Enable APIs & Services**.
   - Search for **Gmail API** and enable it.
4. **Create Service Account**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > Service Account**.
   - Fill in the details and click **Done**.
5. **Generate a JSON Key File**:
   - Click on the created service account.
   - Go to **Keys** and click **Add Key > Create New Key**.
   - Select **JSON** and download the file.
6. **Grant Domain-Wide Delegation**:
   - Go to **Admin Console**: [Google Admin](https://admin.google.com/)
   - Navigate to **Security > API Controls > Domain-Wide Delegation**.
   - Click **Add new**.
   - Enter the **Client ID** from the JSON key.
   - Enter the following OAuth scopes:
     ```
     https://www.googleapis.com/auth/gmail.settings.basic
     https://www.googleapis.com/auth/gmail.settings.sharing
     ```
   - Click **Authorize**.

---

## **3. Database Configuration**
The script fetches user details from a MySQL database. You need to update the database credentials in `update_signature.py`:

```python
mydb = mysql.connector.connect(
  host="your_database_host",
  user="your_database_user",
  password="your_database_password",
  database="your_database_name"
)
```

---

## **4. Running the Script**
### **Step 1: Clone the Repository**
```sh
git clone https://github.com/bharatcj/google-signature-updater.git
cd google-signature-updater
```

### **Step 2: Run the Script**
```sh
python3 update_signature.py <user_id>
```
Replace `<user_id>` with the actual user ID from your database.

---

## **5. Error Handling**
If an error occurs while updating the signature, the script:
- Retries the update up to **3 times** if a temporary error occurs.
- Prints error messages for debugging.
- Logs failed attempts for later review.

---

## **6. Customization**
- Modify the **signature template** in the script to match your company’s branding.
- Update **database queries** if your schema is different.

---

## **7. License**
This project is licensed under the **MIT License**.

---

## **8. Contributing**
Contributions are welcome! Feel free to fork this repository and submit pull requests.

---

### **Author**
Developed by **[Your Name]**  
GitHub: [Your GitHub Profile](https://github.com/bharatcj)
```