import requests
import os
from utils.logger import logger
from dotenv import load_dotenv
load_dotenv()

ig_profile_link = os.getenv("IG_PROFILE_LINK")
ig_link = f"📸 Instagram: {ig_profile_link}"

fb_profile_link = os.getenv("FB_PROFILE_LINK")
fb_link = f"📘 Facebook: {fb_profile_link}"

client_id = os.getenv("LINKEDIN_CLIENT_ID")
client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")

refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")

def post_to_linkedin(image_path, formatted_message, hashtag):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    try:
        validated_token= validate_and_renew_access_token(access_token)
        organization_urn = f"urn:li:organization:{os.getenv('LN_PAGE_ID')}"
        post_text = formatted_message + "\n\n" + fb_link + "\n\n" + ig_link + "\n\n" + hashtag

        # 1. Initialize upload
        init_response = initialize_image_upload(organization_urn, validated_token)
        upload_url = init_response["uploadUrl"]
        image_urn = init_response["image"]

        # 2. Upload image bytes
        upload_success = upload_image_bytes(upload_url, image_path, validated_token)
        if not upload_success:
            logger.error("Failed to upload image bytes")
            return None

        # 3. Post content referencing uploaded image
        post_response = post_linkedin_image_post(organization_urn, image_urn, "Image description", post_text, validated_token)

        return post_response
    except Exception as e:
        logger.error(f"LinkedIn posting failed: {e}")


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

    return resp.json()["value"]  # contains uploadUrl and image URN

def upload_image_bytes(upload_url, image_path, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    with open(image_path, "rb") as f:
        data = f.read()
    resp = requests.put(upload_url, headers=headers, data=data)
    resp.raise_for_status()
    return resp.status_code == 200 or resp.status_code == 201

def post_linkedin_image_post(organization_urn, image_urn, alt_text, post_text, access_token):
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202506"
    }
    post_text = post_text.replace("(", "（").replace(")", "）")
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



def validate_and_renew_access_token(access_token):

    # Try current token first
    test_url = "https://www.linkedin.com/oauth/v2/introspectToken"

    # Form data to send in the POST request
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token": access_token  # Your actual token here
    }
    resp = requests.post(test_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if resp.status_code != 200:
        return refresh_linkedin_token()

    data = resp.json()   # 👈 parse JSON body

    if not data.get("active", False):   # token expired or inactive
        return refresh_linkedin_token()

    return os.environ["LINKEDIN_ACCESS_TOKEN"]

def refresh_linkedin_token():
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
        if tokens['access_token']:
            new_token = tokens['access_token']
            logger.info("LinkedIn token updated successfully")
            os.environ["LINKEDIN_ACCESS_TOKEN"] = new_token
            # global  access_token
            #access_token = new_token
        if tokens['refresh_token']:
            logger.info("LinkedIn refresh_token updated successfully")
            os.environ["LINKEDIN_REFRESH_TOKEN"] = tokens['refresh_token']
        return new_token
    else:
        raise Exception(f"Failed to refresh token: {response.status_code} {response.text}")


# image = "/Users/pmahajan/Downloads/googlee.png"
# # # Read the image file as raw bytes
# # with open(image, "rb") as image_file:
# #     image_bytes = image_file.read()
# # if image_bytes:
# result = post_to_linkedin_with_image(image, "Test Instagram post from AI News")
# print(result)



