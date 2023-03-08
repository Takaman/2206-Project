from feedsearch import search
import feedparser
import time

#11 feeds in list
feeds_list = [
"https://www.rfa.org/english/RSS",
"https://thediplomat.com/feed",
"https://e27.co/index_wp.php/feed/",
"https://www.asianscientist.com/feed/?x=1",
"http://www.asianage.com/rss_feed/",
"https://www.newmandala.org/feed/",
"https://www.asiasentinel.com/feed/",
"https://asia.nikkei.com/rss/feed/nar",
"http://www.scmp.com/rss/91/feed",
"https://www.channelnewsasia.com/rssfeeds/8395986",
"https://asean.org/feed/",
]

feeds = search(feeds_list[6])
urls = [f.url for f in feeds]

if len(urls) > 0:
  news_feed = feedparser.parse(urls[0])
  entries = news_feed["entries"]
  count=0
  for entry in entries:
    count = count + 1
    print(str(entry["title"]))
    if count==5: # modify this value to increase article count
        break
    time.sleep(0.33)