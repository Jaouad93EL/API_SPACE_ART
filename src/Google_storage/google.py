from google.cloud import storage
from google.oauth2 import service_account
from requests_oauthlib import OAuth2Session

google_config = {
    "type": "service_account",
    "project_id": "spaceart-238712",
    "private_key_id": "ccbd248ec09ba3d6387881ff1d85220ae0ea8bd0",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDhabNzOC9j4C8P\nw7tAvYN0ZhpHStfBvuHmikOtBEOIp0cJ9X77Y4Yrn+n2BYxqja5oJypn2nUDdieS\nDlAdPNYP12CD9OVlZoMMalc43XqJOvQm12qFgJTpw2FCwD50xyO+sEu0KJWZCJZD\n56YXOKp9a9GAC3qXGRloouY7Vmtz5NeRtRGwes4CgrqBLSy0FYhBW2yGvguw/SQc\nIAYpRgXSS5eq5e2sdU+sdxhbXmEwkBMxmB0JSuVM1YLEPb7DMM1HMWLzmlaY3ZGL\nYjbiLdmhGVXRwZgbaLiFCrKX3nUpd3bg/Cn1cyOWz9H6zuwV/igLLDWI1Cj1UQst\ng0lzKeI5AgMBAAECggEAAebU4z0PNUrMyteOMSq7VnrBo2Yi8aXNHRdMhxCl2AJl\nRVTwLpz1b4SVW9FKXaz27Dafk0NS2mXsSb11X16S7CZKg6jhjvXxV0qSx5sivGnZ\naalGlkklhUVaZ2hDMdQEqq6tEzns05IwrL9iQm7kpuzUCYsCcttJpuOjVc8FI0Cm\nb8GJYv6xUeBYG18Aa/8x8WVBrsitZgVW55WAM7PTGSw3NCH05HVd1bIq8CjJQz99\nrqengoZvSMYKbe/ZFLSbcBPGMTEk2oorBLTzpyw4RIUkqDPCa/gu4QH2geFptmYT\npg8Dbb2MtLNGKa/FB3onKAHRZlOaH5G4dDT+DcH5owKBgQD5bhgNHjg6TSdL58MW\njk81fnD9/JgyENbFKKBqEMTkCUjncGtmNWy3DYDnslCzkqLgOl6fFz1PVq/EJ5SX\noJS6HDjHM73Fs5Exzne8WiT3x/dKl3bdynsxG+mL1FwL0uA/A2SsTqfgt3YqZfa0\nvrnQahrtJrTxrLTj9vGpJ+rmpwKBgQDnWajOD2Az+L4D6fmIANGCgJzLZr7uLyg2\nDmWkJpFWSslg2Holq2tcKzUNLlf7S3BnLCFK7lQNUo2ksY2YaOaNvBLr9YISdFAk\nztkuNyisKp5H6GCSKNQiJ2iWYEa7eKxm++Pwr3ZelXZswCrnK+/rZSpf+fFyeFOK\nv42R3vrsHwKBgGJG7JcOlxzxlVAlCwryG2d6YE7SnazsUZLxRPNFlC49MkpuUwK8\nfg9J9MZVzdJTLnWmye1pHLEL+MkSx0tO7ArAX+atDlK9Q7IaJbdC1VoDof3z29Pb\nmdppowWDMJlABzcMwTfa7e5umtJtxlzE4TWq+N0D6TtnzwYbIHCD19v1AoGAaQUE\nYfYM38rMxw4RXjGw6aLkiljr10fE4zUJ4sg3NYrhe3sJh8wXAlIC1SbyfXqzXcJk\nopUpxppw/hAzjLoh3rk/hal/EE2IjAzx/c7AQdde3pmYLQEnuxFUot61fSi8akty\nH7Im86y5g4iAcUw6rwrPf54AgswocFWgOFWWZlUCgYEA6vXt9FL5qWgytkU/mNbW\n7Rxqa6+ulJSU4JehXEt1aW8pAXFjVyVKsk25nDj/BBZDYllPMOj8ft4jUGwCQyNg\nK3v7RWRhpcGn1R5Gj52FyEn4rvlaw8CeIvCW3zkq8E+P5rI/alvZepkU/pGWBSBY\nUH8F5FUHaCAQ9HdbhloO+OA=\n-----END PRIVATE KEY-----\n",
    "client_email": "spaceart@spaceart-238712.iam.gserviceaccount.com",
    "client_id": "110358215360033227158",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/spaceart%40spaceart-238712.iam.gserviceaccount.com"
}

CLIENT_ID = '354503433014-dt8bat8cgaosk5ci76qquc13vgv2ofb9.apps.googleusercontent.com'
CLIENT_SECRET = 'JslKPgWYdc-sHwXD1Rla784y'
REDIRECT_URI = 'https://127.0.0.1:5000/api/users/gCallback'
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
SCOPE = ['profile', 'email']

project_id = 'spaceart-238712'
google_unauthorized = 'kenzazerouali00@gmail.com'
storage_credentials = service_account.Credentials.from_service_account_info(google_config)
storage_client = storage.Client(project=project_id, credentials=storage_credentials)

def get_google_auth(state=None, token=None):
    if token: return OAuth2Session(CLIENT_ID, token=token)
    if state: return OAuth2Session(
        CLIENT_ID,
        state=state,
        redirect_uri=REDIRECT_URI)
    your_oauth = OAuth2Session(
        CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE)
    return your_oauth

def store_in_google(bucket_name, id_rep, file):
    bucket = storage_client.get_bucket(bucket_name)
    up_file = bucket.blob(id_rep + '/' + file.filename)
    up_file.upload_from_string(file.read(), content_type=file.content_type)
    return up_file.public_url

def delete_in_google(bucket_name, id_rep, file_name):
    bucket = storage_client.get_bucket(bucket_name)
    del_file = bucket.blob(id_rep + '/' + file_name)
    del_file.delete()

def delete_user_google(user_id):
    li = ['audio_space_art', 'banner_space_art', 'picture_space_art', 'video_space_art']
    for l in li:
        bucket = storage_client.get_bucket(l)
        del_rep = bucket.blob(user_id + '/')
        del_rep.delete()