import os
from client.aws_s3 import upload_image_to_s3
from utils.logger import logger
from facebook import  GraphAPI,GraphAPIError

instagram_account_id = os.getenv("IG_ACCOUNT_ID")

ln_profile_link = os.getenv("LN_PROFILE_LINK")
ln_link = f"🔗 LinkedIn: {ln_profile_link}"

fb_profile_link = os.getenv("FB_PROFILE_LINK")
fb_link = f"📘 Facebook: {fb_profile_link}"

access_token = os.getenv("FB_ACCESS_TOKEN")
graph = GraphAPI(access_token)

def post_to_instagram(image_bytes: bytes, formatted_message: str, hashtag):


    #upload image to s3
    public_url = upload_image_to_s3(image_bytes)
    if not public_url:
        logger.error("Failed to upload image to s3")
        return {"Instagram": "Failed"}
    #public_url = "https://news--image.s3.ap-southeast-1.amazonaws.com/c49bfdda34934708bbe512fae1467b14.jpg"
    # Post to Instagram
    try:
        container = graph.put_object(
            instagram_account_id,
            "media",
            image_url=public_url,
            media_type="IMAGE",
            caption=formatted_message[:2000] + "\n\n" + fb_link + "\n\n" + ln_link + "\n\n" + hashtag,
        )

        import time
        if container and 'id' in container:
            time.sleep(5)  # Wait for container processing
            insta = graph.put_object(
                instagram_account_id,
                "media_publish",
                creation_id=container['id']
            )
            return insta
        else:
            logger.error("Instagram container creation failed")
            return {"Instagram": "Failed"}
    # except GraphAPIError as e:
    #     logger.error(f"Instagram GraphAPIError error: {str(e)}")
    #     return {"Instagram": "Failed"}
    except Exception as e:
        logger.error(f"Instagram posting failed: {e}")
        return {"Instagram": "Failed"}


# image = "/Users/pmahajan/Downloads/googlee.png"
# # # Read the image file as raw bytes
# with open(image, "rb") as image_file:
#     image_bytes = image_file.read()
# if image_bytes:
#     result = post_to_instagram(image_bytes, "Test Instagram post from AI News")
#     logger.info(result)

# import requests
# r = requests.head("https://i.ibb.co/ccYSS06q/c7f31530307c.jpg")
# print(r.headers.get("Content-Type"))  # Should print 'image/png'
