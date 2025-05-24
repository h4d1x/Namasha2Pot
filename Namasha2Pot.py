import sys
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import requests
from bs4 import BeautifulSoup
import subprocess
import re
import os
import pyperclip
import configparser
import tempfile
import pyperclip
import sys
from urllib.parse import urlparse

#config.ini
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)
edge_driver_path = config.get('Paths', 'edge_driver_path')
potplayer_path = config.get('Paths', 'potplayer_path')
try:
    perfer_quality = int(config.get('Settings', 'perfer_quality'))
except ValueError:
    perfer_quality = 720 
print("Edge Driver Path:", edge_driver_path)
print("PotPlayer Path:", potplayer_path)
print("Preferred Quality:", perfer_quality)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu") 
options.add_argument("--mute-audio") 
options.add_argument("--log-level=3")
prefs = {
    "profile.managed_default_content_settings.images": 2,  
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.media": 2 
}
options.add_experimental_option("prefs", prefs)
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)
def get_subtitle_link(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jwplayer'))
        )
        print("jwplayer!")
    except:
        print("jwplayer Is Dead!")
        driver.quit()
        return None
    
    script = """
    const config = jwplayer().getConfig();
    if (config && config.captionsTrack) {
        const captionsTrack = config.captionsTrack;
        if (captionsTrack.kind === "captions" && captionsTrack.file) {
            return captionsTrack.file;
        }
    }
    return null;
    """
    try:
        subtitle_link = driver.execute_script(script)
        if subtitle_link:
            print("Sub Links :", subtitle_link)
        else:
            print("No Sub!")
        return subtitle_link
    except Exception as e:
        print(f"Error WTF!: {e}")
        return None
def get_best_video_link(prefer_quality, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True, class_='action-menu-item')
    print(f"[DEBUG] Found {len(links)}Q")
    video_links = {}
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        match = re.search(r'(\d{3,4})p', text)
        if match:
            quality = int(match.group(1))
            video_links[quality] = href
            print(f"[DEBUG] Found quality {quality}p")
    if not video_links:
        print("[!] No video links found in page. Let me Handle this...")
        mp4_match = re.search(r'https://s\d+\.namasha\.com/videos/\d+\.mp4', response.text)
        if mp4_match:
            mp4_url = mp4_match.group(0)
            video_url = way2getvideo_link(prefer_quality, mp4_url)
            print(f"[DEBUG] Fallback link generated: {video_url}")
            return video_url
        else:
            print("[X] No MP4 link found in page source. JWPlayer may be hiding it.")
            return None
    if prefer_quality in video_links:
        selected_quality = prefer_quality
    else:
        selected_quality = max(video_links.keys())
        print(f"[!] Preferred quality not found. Falling back to highest: {selected_quality}p")
    video_url = video_links[selected_quality]
    print(f"[+] Quality: {selected_quality} | Final URL: {video_url}")
    return video_url
def way2getvideo_link(prefer_quality, url):
    print(f"[DEBUG] Entered fallback builder with URL: {url}")
    match = re.search(r'https://s(\d+)\.namasha\.com/videos/(\d+)\.mp4', url)
    if not match:
        print("[X] Regex didn't match fallback MP4 link.")
        return None
    server_number = match.group(1)
    video_id = match.group(2)
    print(f"[DEBUG] Extracted server: {server_number}, video ID: {video_id}")
    video_url = f"https://s{server_number}.namasha.com/dash/{video_id}/{prefer_quality}p_dashinit"
    return video_url	   
def download_subtitle_to_temp(subtitle_url):
    if not subtitle_url:
        return None
    try:
        response = requests.get(subtitle_url)
        response.raise_for_status()
        tmp_dir = tempfile.gettempdir()
        subtitle_path = os.path.join(tmp_dir, "subtitle.vtt")
        with open(subtitle_path, 'wb') as f:
            f.write(response.content)
        return subtitle_path
    except Exception as e:
        print("THIS VIDEO HAVE NO SUB!", e)
        return None
def play_in_potplayer(potplayer_path, video_url, subtitle_path=None):
    if subtitle_path and not os.path.exists(subtitle_path):
        subtitle_path = None
    bat_file_path = os.path.join(os.getenv('TEMP'), 'play_video.bat')
    with open(bat_file_path, 'w', encoding='utf-8') as bat_file:
        if subtitle_path:
            bat_file.write(f"""
@echo off
set video_url={video_url}
set subtitle_path={subtitle_path}
set potplayer_path={potplayer_path}

start "" "%potplayer_path%" "%video_url%" /sub="%subtitle_path%"

exit
""")
        else:
            bat_file.write(f"""
@echo off
set video_url={video_url}
set potplayer_path={potplayer_path}

start "" "%potplayer_path%" "%video_url%"

exit
""")
    subprocess.Popen(bat_file_path, shell=True)
    time.sleep(2)  # مدت زمانی که به فایل Batch برای اجرا داده می‌شود
    os.remove(bat_file_path)
url = pyperclip.paste()
if url.startswith("https://www.namasha.com/v"):
    parsed_url = urlparse(url)
    base_url = parsed_url._replace(query="").geturl()
    print("OK WE GOT THIS:", base_url)
else:
    print("NO LINK!")
    sys.exit()
subtitle_link = get_subtitle_link(url)
driver.quit()
subtitle_path = download_subtitle_to_temp(subtitle_link)
video_link = get_best_video_link(perfer_quality,url)

if video_link and subtitle_path:
    play_in_potplayer(potplayer_path, video_link, subtitle_path)
elif video_link:
    play_in_potplayer(potplayer_path, video_link)