import urllib2
from BeautifulSoup import BeautifulSoup
from socket import *
import fileinput
from yandex_translate import YandexTranslate
from threading import Thread

translate = YandexTranslate('yandex.key')

max_threads = 10
current_threads = 0

def main():
	global max_threads
	global current_threads
	with open('sites.lst', 'rb') as f:
		domains = [d.strip() for d in f.readlines()]

	for l in domains:
		while True:
			if current_threads < max_threads:
				t = Thread(target=do_stuff, args=(l,))
				current_threads += 1
				t.start()
				break


def do_stuff(domain):
	global current_threads
	try:
		soup = BeautifulSoup(urllib2.urlopen("http://" + domain, timeout=5))
		title = str(soup.title.string)
		title = title.strip()
	except timeout, e:
		title = "Unavailable Site"
	except urllib2.HTTPError, error:
		title = "Unavailable site"
	except urllib2.URLError, error:
                title = "Unavailable site"
	except:
		title = "Blank or Unreadable Title"
	try:
		if translate.detect(title) != "en":
			trans = translate.translate(str(soup.title.string), 'en')
			titlen = trans['text'][0]
		else:
			titlen = str(title)
	except:
		titlen = "Blank or Unreadable"
	try:
		print ("[-] Title for URL http://" + str(domain) + " is = " + titlen)
	except:
		print ("[-] Title for URL http://" + str(domain) + " is = Blank or Unreadable")
	current_threads -= 1

if __name__ == "__main__":
	main()
