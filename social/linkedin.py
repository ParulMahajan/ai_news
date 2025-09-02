import requests
import os
from utils.logger import logger

ig_profile_link = os.getenv("IG_PROFILE_LINK")
ig_link = f"📸 Instagram: {ig_profile_link}"

fb_profile_link = os.getenv("FB_PROFILE_LINK")
fb_link = f"📘 Facebook: {fb_profile_link}"

def initialize_image_upload(organization_urn, access_token):
    url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202506"
    }
    payload = {
        "initializeUploadRequest": {
            "owner": organization_urn
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["value"]  # contains uploadUrl and image URN

def upload_image_bytes(upload_url, image_path, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    with open(image_path, "rb") as f:
        data = f.read()
    resp = requests.put(upload_url, headers={"Content-Type": "application/octet-stream"}, data=data)
    resp.raise_for_status()
    return resp.status_code == 200 or resp.status_code == 201

def post_linkedin_image_post(organization_urn, access_token, image_urn, alt_text, post_text):
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202506"
    }
    payload = {
        "author": organization_urn,
        "commentary": post_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "content": {
            "media": {
                "id": image_urn,
                "altText": alt_text
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp

def post_to_linkedin_with_image(image_path, formatted_message):

   try:
        access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        organization_urn = f"urn:li:organization:{os.getenv('LN_PAGE_ID')}"
        post_text = formatted_message + "\n\n" + fb_link + "\n\n" + ig_link

        # 1. Initialize upload
        init_response = initialize_image_upload(organization_urn, access_token)
        upload_url = init_response["uploadUrl"]
        image_urn = init_response["image"]

        # 2. Upload image bytes
        upload_success = upload_image_bytes(upload_url, image_path, access_token)
        if not upload_success:
            logger.error("Failed to upload image bytes")
            return None

        # 3. Post content referencing uploaded image
        post_response = post_linkedin_image_post(organization_urn, access_token, image_urn, "Image description", post_text)
        return post_response
   except Exception as e:
       logger.error(f"LinkedIn posting failed: {e}")





def refresh_linkedin_token(refresh_token, client_id, client_secret):
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    if response.ok:
        tokens = response.json()
        return tokens['access_token'], tokens.get('refresh_token', None)
    else:
        raise Exception(f"Failed to refresh token: {response.status_code} {response.text}")