from google.cloud import storage
from google.oauth2 import service_account
from requests_oauthlib import OAuth2Session

google_config = {
  "type": "service_account",
  "project_id": "space-art-249220",
  "private_key_id": "14eb7084d081ac42a9575380e99b0ff12e0170a7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC94JYUqZIXi8GO\n24M0N/aHEcB9kyn5FVaa/hvZLXKZWRhnuA13U5v9xmvw5cDaWoWSBjLd6kGxhLTx\ntw/CvVLGBVr5IAEiCPMcfIXIV7a8tF0Z5Hgpt9N/XY8O9y2bUFYFvzT6Ityorvyh\nfYa3g93wvzNwHjpm5EHIZedRb68LUn6YvdgQSYcR9I24MR4BWBGYBaT8OcewVZ9j\nS+W/dogE07hfvVwaMLADRff0iTy/lzb+FPxbm4HoS2HCCgYWpAFl7IxuX03daw2i\nKIIs8hogkP5sqDG4dMZwU+9QFfsoTLpML6DuVKTyBAnCSUkYPW5WsIdm+QwXpIMR\nUAs/nb+xAgMBAAECggEAAsIAsAlj+LFUFP75dYBUFXNjrjc9WnOtw7fJ4AJF2jYV\n8Yi18lwdpYaUogW2Qr2il8O9CKXawSkuJx4bbZ7KFVv1za1CMvQ6Erl4yHeErRI6\nEXKU77curFiHp8YdjJZSv4fezTzFI3KSMwbDloYE6taeGMRpoP2y+mYHgXJrspCA\nZGOVe1Iq4WkEWWo7X1ggLVN80S1im+eyEC9kPwklLkMQuW93ZuPlZQvwWMNWhFQf\nvurox5PlwtKBTy6wUy0N2Z0yIpbCKfEpziBjgpQQ5NvNVcLttVWQJJVJnwOyMZ5+\nFyNIvtn8SjNhjpBSgOZOFObtGILN9LA4IzvBo4EYmQKBgQDdn8m9LDuN9qwDBr11\nwJTTvolknigonVWQEweOysYhegjkuSwB21aKUL328yL0No1pRarjEIhdGColH374\nCjHdOlZhmr1MHW2C6MYIibG5+2AOIMl++YRkdSYap18PjTBXtEKqPnBzDloNVo/O\nME1TH+UDwjOr2g3XfFwXvaXGKQKBgQDbVDLng8Q6gYr31cVWrPIILL8C+HRyuLAg\nBSSoD8fXWuNN4o7XYEn8BtKHn9MQC863jhTbrNrpLtxRh0eU9bgX0iaW/+cOo5AE\nAbY20HJwo2g4ucvylS4LRmafoTMdrdHMSVxe94Cl41leTBbJAgJ3eRZZIksVRlDT\nVLQ/ArIOSQKBgQCk3cZkrPAMtrDVe4EbhMzyC+8HY8Q6GnjZOd7Icb4cjzzocXv0\nUae6M0Bt4gdhpudhpcrvKZBXuK85eImqmWLo0QoLh+JEKiwaU3FmTpBg60hUmj1q\n8NF1LdTPxSypU/3fcKCbJuHeJZIGFBvcZgBP0w0505E+yXK8l62ml5UnqQKBgFiM\nfty/cwrX4B48/SYIPtMUFa4CVyk17U2QJgOAE4ObmyeHr3m+0z/gFUFSQmk5CyVK\nRJuIBv2bwLFdt4WpSsC7RH80I7niSTOE6Wbp8zoMjvhP8somdmdw7d/GuhdiZNBg\nUd25eQQAbMVIXO6cVBieF2q3EK8vK1SW3wqNcQuZAoGAJTAH4hXmGiEyhzq5bfFl\nYO2oW3i7N7bSRraiua9/+/voO3oPAh5UQ3Hm3SN/tebChqPb2UhfRlCzv6CZLWRA\nERv1UJI1mOyAtZCRET1ux8c1FqScbn+wUBlFi44qZkcLAm5wi11clsOiZ8Owse9I\nQMVeuVLanmiFvc+fBZFlcos=\n-----END PRIVATE KEY-----\n",
  "client_email": "space-art@space-art-249220.iam.gserviceaccount.com",
  "client_id": "113730196016364804583",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/space-art%40space-art-249220.iam.gserviceaccount.com"
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
    li = ['space_art_audio', 'space_art_banner', 'space_art_picture', 'space_art_video']
    for l in li:
        bucket = storage_client.get_bucket(l)
        del_rep = bucket.blob(user_id + '/')
        del_rep.delete()