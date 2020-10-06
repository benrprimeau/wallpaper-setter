from bs4 import BeautifulSoup as bs
import requests
import lxml.html
import urllib
import progressbar

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size, term_width=40)

    downloaded= block_num * block_size
    pbar.start()
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


sub = 'wallpapers'
page = ('https://www.reddit.com/r/' + sub + '/top/?t=day')

headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Referer': 'https://cssspritegenerator.com',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

r = requests.Session().get(page, headers=headers)
soup = bs(r.content, 'html.parser')
print("Opened Connection")

Post_href = soup.find_all('a')
print("Searching soup")

for item in Post_href:
	if '/comments/' in item['href']:
		if 'https://www.reddit.com' in item['href']:
			postURL = item['href']
			print("Secured Post: " + postURL)
			break
		else:
			postURL = 'https://www.reddit.com' + item['href']
			print("Secured Post: " + postURL)
			break

r2 = requests.Session().get(postURL, headers=headers)

try:
	imageSoup = bs(r2.content, 'lxml')

except:
	time.sleep(1)
	imageSoup = bs(r2.content, 'lxml')	

imgs = imageSoup.findAll('a')
print("Browsing Image Links")

srcList = []

for image in imgs:
	try:
#		if str(image['href']).endswith('.jpg') or str(image['href']).endswith('.png'):
		if '.jpg' in str(image['href']) or '.png' in str(image['href']):
			img = image['href']
			break
	except:
		continue

print("Found Image: " + img)
r2.close()
print("Closing Connection")
print("Downloading Image")
urllib.request.urlretrieve(img, '/home/ben/Documents/wall.jpg', show_progress)
print("Download Completed")
