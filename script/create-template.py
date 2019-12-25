import os

WEBSITE = os.environ.get("WEBSITE")
WEBSITE = WEBSITE.rstrip("/")

OSS_BUCKET = os.environ.get("OSS_BUCKET")
OSS_KEYID = os.environ.get("OSS_KEYID")
OSS_SECRET = os.environ.get("OSS_SECRET")
OSS_LINK = os.environ.get("OSS_LINK")

EMAIL_SERVER_HOST = os.environ.get("EMAIL_SERVER_HOST")
EMAIL_SERVER_PORT = int(os.environ.get("EMAIL_SERVER_PORT"))
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")


# 如果你不知道自己在干什么, 不要修改下面的代码

TEMPLATE = f"""
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  Trotter:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: 'serverless comment'
      InternetAccess: true
    Trotter:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Initializer: comment.views.init
        InitializationTimeout: 10
        Handler: comment.app
        Runtime: python3
        CodeUri: './serverless'
        EnvironmentVariables:
          WEBSITE: '{WEBSITE}'
          OSS_BUCKET: '{OSS_BUCKET}'
          OSS_KEYID: '{OSS_KEYID}'
          OSS_SECRET: '{OSS_SECRET}'
          OSS_LINK: '{OSS_LINK}'
          ADMIN_EMAIL: '{ADMIN_EMAIL}'
      Events:
        httpTrigger:
          Type: HTTP
          Properties:
            AuthType: ANONYMOUS
            Methods: ['POST', 'GET']
    SendMail:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Initializer: sendmail.init
        InitializationTimeout: 10
        Handler: sendmail.handler
        Timeout: 60
        Runtime: python3
        CodeUri: './serverless'
        EnvironmentVariables:
          OSS_BUCKET: '{OSS_BUCKET}'
          OSS_KEYID: '{OSS_KEYID}'
          OSS_SECRET: '{OSS_SECRET}'
          OSS_LINK: '{OSS_LINK}'
          EMAIL_SERVER_HOST: '{EMAIL_SERVER_HOST}'
          EMAIL_SERVER_PORT: {EMAIL_SERVER_PORT}
          EMAIL_USERNAME: '{EMAIL_USERNAME}'
          EMAIL_PASSWORD: '{EMAIL_PASSWORD}'
      Events:
        SendMail:
          Type: OSS
          Properties:
            BucketName: {OSS_BUCKET}
            Events:
              - oss:ObjectCreated:*
            Filter:
              Key:
                  Prefix: mail/
                  Suffix: .task
"""

if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "template.yml"), "w+") as yml:
        yml.write(TEMPLATE)
