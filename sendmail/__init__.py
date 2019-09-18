import os
import json
import typing
import pickle
import hashlib
import smtplib
import logging
from email.mime.text import MIMEText
from email.header import Header

import oss2

OSS_BUCKET = os.environ.get("OSS_BUCKET")
OSS_KEYID = os.environ.get("OSS_KEYID")
OSS_SECRET = os.environ.get("OSS_SECRET")
OSS_LINK = os.environ.get("OSS_LINK")
EMAIL_SERVER_HOST = os.environ.get("EMAIL_SERVER_HOST")
EMAIL_SERVER_PORT = int(os.environ.get("EMAIL_SERVER_PORT"))
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


smtpObj = None


def sendmail(nickname: str, to_email: str, subject: str, content: str) -> typing.Tuple[bool, typing.Union[None, str]]:
    """发送邮件通知"""
    global smtpObj

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header(f"Trotter<{EMAIL_USERNAME}>", 'utf-8')
    message['To'] = Header(f'{nickname}<{to_email}>', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj.sendmail(EMAIL_USERNAME, to_email, message.as_string())
        return True, None
    except smtplib.SMTPException as e:
        return False, str(e)


def init(context):
    global smtpObj
    smtpObj = smtplib.SMTP(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    smtpObj.starttls()
    smtpObj.login(EMAIL_USERNAME, EMAIL_PASSWORD)


def handler(event, context):
    evt = json.loads(event)
    bucket = oss2.Bucket(
        oss2.Auth(OSS_KEYID, OSS_SECRET),
        OSS_LINK,
        OSS_BUCKET
    )
    object_name = evt['events'][0]['oss']['object']['key']
    remote_stream = bucket.get_object(object_name)
    remote_stream = remote_stream.read()
    task = pickle.loads(remote_stream)
    res, err = sendmail(**task)
    if err:
        logging.error(err)
    if res:
        bucket.delete_object(object_name)
