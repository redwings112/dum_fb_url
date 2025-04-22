import requests
from bs4 import BeautifulSoup
import re

def download_facebook_reel(url, filename="facebook_reel.mp4"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("[*] Fetching the page...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("[!] Failed to fetch the page.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Look for video tag or og:video meta
    video_url = None

    # Try og:video
    og_video = soup.find("meta", property="og:video")
    if og_video and og_video.get("content"):
        video_url = og_video["content"]
    else:
        # Try to find a direct .mp4 in the page
        match = re.search(r'https://[^"]+\.mp4', response.text)
        if match:
            video_url = match.group(0)

    if not video_url:
        print("[!] Could not find the video URL.")
        return

    print(f"[*] Downloading video from: {video_url}")
    video_data = requests.get(video_url, headers=headers)

    with open(filename, "wb") as f:
        f.write(video_data.content)

    print(f"[+] Downloaded video as {filename}")

# Example usage
fb_reel_url = "https://www.facebook.com/reel/1234567890123456"  # Replace with your actual URL
download_facebook_reel(fb_reel_url)
