from __future__ import print_function
import os.path
import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Replace with the path to your credentials.json file
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'

# Create a service account
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build('drive', 'v3', credentials=creds)

def get_latest_file_id(folder_id):
    # List files in the specified folder
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=10,  # Adjust as needed
        fields="files(id, name, modifiedTime)",
        orderBy="modifiedTime desc"
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print('No files found.')
        return None
    else:
        # Return the ID of the most recently modified file
        latest_file = items[0]
        print(f"Latest file: {latest_file['name']} (ID: {latest_file['id']})")
        return latest_file['id']

def download_file(file_id, destination):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

if __name__ == '__main__':
    folder_id = 'your_folder_id_here'  # Replace with the ID of your Google Drive folder
    destination = '/path/to/your/local/folder/filename.xlsx'  # Replace with the destination path

    # Get the ID of the most recently updated file in the folder
    latest_file_id = get_latest_file_id(folder_id)
    
    if latest_file_id:
        # Download the most recent file
        download_file(latest_file_id, destination)