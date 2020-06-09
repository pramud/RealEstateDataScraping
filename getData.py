import requests
import time
from bs4 import BeautifulSoup

def get_listing_details(pageNumber):
    page_listings = []
    pageNumber = str(pageNumber)
    a = requests.get(base_url + pageNumber)
    html= BeautifulSoup(a.text,'html.parser')
    all_ele = html.find_all("div", class_="cardWrapper")
    for ele in all_ele:
        listing = {}
        price = None
        area = None
        status = None
        others = []
        keypointers = []
        for i,row in enumerate(ele.find_all("tr", class_ = "hcol")):
            if i == 0:
                price = row.get_text()
            elif i ==1:
                area = row.get_text()
            elif i ==2:
                status = row.get_text()
            else:
                others.append(row.get_text())
        rera = ele.find(class_= 'rera-tag-new')
        if rera:
            rera = rera['title']
        else:
            rera = None
        for keypoints in ele.find_all(class_= 'keypoint'):
            keypointers.append(keypoints.get_text())
        listing["link"] = ele.find(class_= 'title-line').find("a")['href']

        listing["loc"] = ele.find(class_= 'locName').get_text()
        listing["title"] = ele.find(class_= 'title-line').get_text()
        listing["price"] = price
        listing["area"] = area
        listing["status"] = status
        listing["rera"] = rera
        listing["keypointers"] = keypointers
        page_listings.append(listing)
    return page_listings

all_listings = []
total_pages = 1791
base_url = 'https://www.makaan.com/hyderabad-residential-property/buy-property-in-hyderabad-city?page='
for page in range(1, total_pages+1):
    listings = get_listing_details(page)
    all_listings.extend(listing)
    print("processed page ", page, listings[0], "total litings ", len(all_listings)) 
    time.sleep(2)
