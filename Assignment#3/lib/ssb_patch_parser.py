from selenium import webdriver

class SSB():
    def __init__(self):
        self.name = "Super Smash Bros"
        self.names = ["SSB", "ssb"]
        self.patch = {"title": None, "url": None, "desc": None, "image": None}
        self.color = 16744448
        self.thumbnail = "https://i.imgur.com/OViQbBo.png"
        self.get_latest_patch_info()

    def get_latest_patch_info(self):

        # Gets source of Counter-strike's blog.
        driver = webdriver.Chrome()
        op = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=op)
        try:
            driver.get("https://www.smashbros.com/en_US/blog/index.html")
            assert "Super" in driver.title
            blogItems = driver.find_elements_by_class_name("blog-item")
            assert "No results found." not in driver.page_source

            print("yep")
        except:
            raise Exception("Couldn't connect to " + self.name + "'s website.")

        try:

            for blog in blogItems:
                self.patch["desc"] = blog.text
                print("Blog Text: {}".format(blog.text))
                break
        except:
            raise Exception("Couldn't get blog info")
        driver.close()



if __name__ == '__main__':
    ssb = SSB()
    ssb.get_latest_patch_info()