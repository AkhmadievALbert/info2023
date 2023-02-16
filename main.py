from spider import Spider

if __name__ == '__main__':
    base_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html"
    nested_link_class = "reference internal"
    spider = Spider(base_url, nested_link_class)
    spider.start_parsing()
