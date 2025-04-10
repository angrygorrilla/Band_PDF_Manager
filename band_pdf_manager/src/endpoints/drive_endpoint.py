import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth
from googleapiclient.http import MediaIoBaseDownload
import io

def download_file(real_file_id):
  """Downloads a file
  Args:
      real_file_id: ID of the file to download
  Returns : IO object with location.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds=get_creds()

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    file_id = real_file_id

    # pylint: disable=maybe-no-member

    request = service.files().export_media(fileId=file_id, mimeType='application/pdf')

    #request = service.files().get_media(fileId=file_id)
    print(request)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}.")

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

    with open('file.pdf','wb') as f:
      f.write(file)
  return file

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

#get the top n files
def top_file_folders(number_of_files):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds=get_creds()

  try:
    service = build("drive", "v3", credentials=creds)
    
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=number_of_files, 
              fields="nextPageToken, files(id, name)",
              )
        .execute()
    )

    #query terms
        #mimeType = 'application/vnd.google-apps.folder'
        #Files within a collection (for example, the folder ID in the parents collection)

    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    #items from this api include a name and an id
    for count,item in enumerate(items):
        print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

#search for users file folder
def search_folders(name,folder=True):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds=get_creds()

  try:
    service = build("drive", "v3", credentials=creds)
    qustion=None
    if folder==True:
        question=f"mimeType='application/vnd.google-apps.folder' and name='{name}'",
    elif folder==False:
        question=f"name='{name}'",


    # Call the Drive v3 API
    results = (
        service.files()
        .list(fields="nextPageToken, files(id, name)",
              q=question,
              )
        .execute()
    )

    #query terms
        #mimeType = 'application/vnd.google-apps.folder'
        #Files within a collection (for example, the folder ID in the parents collection)

    items = results.get("files", [])
    #items from this api include a name and an id
    for count,item in enumerate(items):
        print(f"{item['name']} ({item['id']})")
    return(items)
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


#download all files from a folder
def download_folder_contents(id):
    return None



#use a google token saved in json format to certify using google drive apis
def get_creds():
    # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds=None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    #with open("secrets/token.json", "w") as token:
    #  token.write(creds.to_json())
    return creds

if __name__ == "__main__":
  #print(search_folders('Resume',folder=False))
  #top_file_folders(999)
  #17pnOs4CbKGzDIK0FTmAU-6MoId8gjWwF
  download_file('14mdta9XO2E2oZAE-zFKph_Lb0xio0Xls')

 

  #download file does not work on folder - need to do a parent search using it
  #example of folder to take files from:
  #GCB FALL - TUBA (1X7tY37gwMj4otUOYMo98wO31NOgqucOZ)


#id's from the other service don't seem to work - need to look into
  #example of a file: when robins appear (1naNF8R2M0BdpiZF1Q60Ax_yA1Re7LKdk)
  #download_file('1naNF8R2M0BdpiZF1Q60Ax_yA1Re7LKdk')