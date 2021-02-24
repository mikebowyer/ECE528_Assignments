import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


def getLatestAccouncement(url):
    latestAccouncement = {"title": None, "info": None, "date": None, "url": None, "img_url": None}

    # Make request to grab community news from steam
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        source = urlopen(request).read()
        bsoup = soup(source, "html.parser")
        announcmentCards = bsoup.findAll('div', {'class': lambda x: x and 'Announcement_Card' in x.split()})
    except:
        raise Exception("Couldn't connect connect to URL.")

    # get latest anncouncment card information
    try:
        latestAccouncement["title"] = \
        announcmentCards[0].findAll("div", class_="apphub_CardContentNewsTitle")[0].contents[0]
        latestAccouncement["date"] = announcmentCards[0].findAll("div", class_="apphub_CardContentNewsDate")[0].text
        latestAccouncement["img_url"] = announcmentCards[0].findAll("img")[0].attrs["src"]
        latestAccouncement["url"] = announcmentCards[0].attrs["data-modal-content-url"]

        # contents = announcmentCards[0].findAll("div", class_="apphub_CardTextContent")[0].contents
        # resultStr = ""
        # for element in contents:
        #     elemStr = str(element)
        #     if elemStr == '<br/>':
        #         elemStr = '\n'
        #     resultStr = resultStr + elemStr

        latestAccouncement["info"] = announcmentCards[0].findAll("div", class_="apphub_CardTextContent")[0].get_text(separator="\n")
    except:
        raise Exception("Error retrieving annoucnment information title.")

    return latestAccouncement
