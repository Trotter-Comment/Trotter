import os

WEBSITE = os.environ.get("WEBSITE")
assert WEBSITE, "WEBSITE must be set in os.environ"
WEBSITE = WEBSITE.strip("/")

OSS_BUCKET = os.environ.get("OSS_BUCKET")
assert OSS_BUCKET, "OSS_BUCKET must be set in os.environ"

OSS_KEYID = os.environ.get("OSS_KEYID")
assert OSS_KEYID, "OSS_KEYID must be set in os.environ"

OSS_SECRET = os.environ.get("OSS_SECRET")
assert OSS_SECRET, "OSS_SECRET must be set in os.environ"

OSS_LINK = os.environ.get("OSS_LINK")
assert OSS_LINK, "OSS_LINK must be set in os.environ"
