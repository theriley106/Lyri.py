import requests
import bs4
import shutil
import re
import os
import eyed3
import random
#Requires FFMpeg, YoutubeDL
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
proxies = {}

def DownloadAlbumArt(URL):
	FileName = "{}.jpg".format(str(random.randint(100000, 10000000)))
	response = requests.get(URL, stream=True)
	with open(FileName, 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	return FileName

def DownloadMusic(URL):
	FileName = str(random.randint(100000, 10000000))
	os.system('youtube-dl --extract-audio --ignore-errors --audio-format mp3 -o "{}.%(ext)s" {}'.format(FileName, URL))
	FileName = "{}.mp3".format(FileName)
	return FileName
def SearchYoutube(string):
	string = string.replace(' ', '+')
	URL = 'https://www.youtube.com/results?search_query={}'.format(string)
	res = requests.get(URL, headers=headers)
	page = bs4.BeautifulSoup(res.text, "lxml")

	Result = page.select('.item-section > li .clearfix')
	Results = []
	for number in Result:
		if 'Duration' in str(number):
			Results.append(number)
	VideoID = str(Results[0].select('.overflow-menu-choice')[0]).partition('data-video-ids="')[2].partition('" onclick="')[0]
	URL = 'https://www.youtube.com/watch?v={}'.format(VideoID)
	print(URL)
	Location = DownloadMusic(URL)
	return Location
	

def SearchSong(string):
	keyword = string.replace(' ', '+')
	URL = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords={}'.format(keyword)
	res = requests.get(URL, headers=headers)
	page = bs4.BeautifulSoup(res.text, "lxml")
	page = page.select('#result_0')[0]
	URL = page.select('.songTitle')
	URL = re.search("(?P<url>https?://[^\s]+)", str(URL))
	URL = str(URL.group("url"))[:-1]
	information = {
	'Title': page.select('.songTitle')[0].getText(),

	'URL': URL,
	'Artist': page.select('.s-music-track-artist')[0].getText(),
	'Album': page.select('.s-music-track-album')[0].getText(),
	'Length': page.select('.s-music-track-time')[0].getText()
	}
	res = requests.get(URL, headers=headers)
	page = bs4.BeautifulSoup(res.text, "lxml")
	AlbumCover = page.select('#coverArt_feature_div')
	URL = re.search("(?P<url>https?://[^\s]+)", str(AlbumCover))
	URL = str(URL.group("url"))[:-1]
	URL = URL.partition('"')[0]
	Image_File = DownloadAlbumArt(URL)
	Audio_File = SearchYoutube('{} {}'.format(information["Title"], information["Artist"]))
	NewFileName = "{} - {}.mp3".format(information["Title"], information["Artist"])
	UpdateInfo(Audio_File, Image_File, information["Album"], information["Artist"], information["Title"], NewFileName)

def UpdateInfo(mp3_file_name, artwork_file_name, album, artist, title, filename):
	audiofile = eyed3.load(mp3_file_name)
	audiofile.tag.images.set(3, open(artwork_file_name,'rb').read(), 'image/jpeg')

	# write it bac
	audiofile.tag.artist = unicode(str(artist), "utf-8")
	audiofile.tag.album = unicode(str(album), "utf-8")
	audiofile.tag.title = unicode(str(title), "utf-8")
	audiofile.tag.save()
	os.rename(mp3_file_name, filename)




