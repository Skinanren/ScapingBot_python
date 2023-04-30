import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# import ssl
# import re
# ssl._create_default_https_context = ssl._create_unverified_context
from scrapingbee import ScrapingBeeClient


archive_url = f"https://www.youtube.com/watch?v=IZuWB_URVEI"
 
def get_video_links():
#     #create response object
#     req = Request(
#             url=archive_url, 
#             headers={'User-Agent': 'Mozilla/5.0'}
#         )
#     html = urlopen(req).read()
        client = ScrapingBeeClient(api_key='4TAO8EV5D7WVT292QPGGEVJY9L4NQC67CJ6WPSW4RDZTEPZIMJOCL0DJH4XP8XCKHXFNWWZRJ6HG6MA1')
        response = client.get(archive_url)
        bs = BeautifulSoup(response.content, "html5lib")
# 
#     bs = BeautifulSoup(html, 'html5lib')
#     # r = requests.get(archive_url)
#     #create beautiful-soup object
#     # soup = BeautifulSoup(r.content,'html5lib')
#     #find all links on web-page
        links = bs.findAll('a')
       #filter the link ending with .mp4
        video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]
        print(video_links)
        
        return video_links
 
# get_video_links()


# def download_video_series(video_links):
 
#     for link in video_links:
#         '''
#         iterate through all links in video_links
#         and download them one by one
#         '''
#         client = ScrapingBeeClient(api_key='4TAO8EV5D7WVT292QPGGEVJY9L4NQC67CJ6WPSW4RDZTEPZIMJOCL0DJH4XP8XCKHXFNWWZRJ6HG6MA1')
#             # response = client.get(siteUrl)
#             # bs = BeautifulSoup(response.content, "html.parser")
#         #obtain filename by splitting url and getting last string
#         file_name = link.split('/')[-1]   
#         print("filename = ",file_name)
#         print ("Downloading file:%s"%file_name)
 
#         #create response object
#         # r = requests.get(link, stream = True)
#         r = client.get(link,stream = True)
#         #download started
#         with open(file_name, 'wb') as f:
#             for chunk in r.iter_content(chunk_size = 1024*1024):
#                 if chunk:
#                     f.write(chunk)
 
#         print ("%s downloaded!\n"%file_name)
 
#     print ("All videos downloaded!")
#     return
 
if __name__ == "__main__":
    #getting all video links
    video_links = get_video_links()
 
    #download all videos
    # download_video_series(archive_url)