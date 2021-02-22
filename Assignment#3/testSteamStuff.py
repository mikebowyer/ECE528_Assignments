import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


if __name__ == '__main__':
    patch = {"title": None, "url": None, "desc": None, "image": None}
    # Gets source of Counter-strike's blog.
    try:
        request = Request("https://steamcommunity.com/app/413150/allnews/", headers={'User-Agent': 'Mozilla/5.0'})
        source = urlopen(request).read()
        bsoup = soup(source, "html.parser")
        main_blog_div = bsoup.findAll("div",{"id":"page1"})
    except:
        raise Exception("Couldn't connect to steams's website.")

    # Gets CSGO's patch title.
    try:
        patch["title"] = main_blog_div[0].div.div.h2.a.contents[0]
        if patch["title"] is None:
            raise Exception("Could not find  title.")
    except:
        raise Exception("Error retrieving  title.")