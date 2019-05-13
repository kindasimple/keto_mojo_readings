#!/usr/bin/env python

from __future__ import print_function
import pickle
import os.path
import logging
import io

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

logging.basicConfig()
logger = logging.getLogger(__name__)


SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.file'
]


def connect():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds, cache_discovery=False)
    return service


def get(service, remote_filename, local_filepath):
    file_id = _find_file_id(service, remote_filename)
    if not file_id:
        raise ValueError('file_id not found')
    _download_file(service, file_id, local_filepath)


def _find_file_id(service, remote_filename):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        logger.info('No files found.')
        return

    for item in items:
        if item['name'] == remote_filename:
            logger.info(
                'Found {0} ({1})'.format(item['name'], item['id'])
            )
            return item['id']


def _download_file(service, file_id, local_filepath):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_filepath, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logger.debug("Download %d%%.", int(status.progress() * 100))


def store(service, remote_filename, local_filepath):
    file_id = _find_file_id(service, remote_filename)

    file_metadata = {'name': remote_filename}
    media = MediaFileUpload(local_filepath,
                            mimetype='text/plain')

    if file_id:
        file = service.files().update(
            body=file_metadata,
            media_body=media,
            fileId=file_id,
            fields='id'
        ).execute()
    else:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
    logger.info('File ID: %s', file.get('id'))


if __name__ == '__main__':
    connect()
