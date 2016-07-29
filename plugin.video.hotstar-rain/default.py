import re, os, sys
import urllib
import urllib2
import json
import requests
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
from addon.common.addon import Addon
import datetime

addon_id = 'plugin.video.hotstar-rain'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
debug = Addon.getSetting('debug')

language = (Addon.getSetting('langType')).lower()
perpage = (Addon.getSetting('perPage'))
moviessortType = (Addon.getSetting('moviessortType')).lower()
enableip = (Addon.getSetting('EnableIP'))
ipaddress = (Addon.getSetting('ipaddress'))
quality = (Addon.getSetting('qualityType')).lower()

dialog = xbmcgui.Dialog()


if moviessortType=='name':
	moviessortType='title+asc'
elif moviessortType=='newest':
	moviessortType='last_broadcast_date+desc'#,year+desc,title+asc'
else:
	moviessortType='counter+desc'
	
if (quality=='let me choose'):
	fold = False
else:
	fold = True

s=requests.Session()

def addon_log(string):
    if debug == 'true':
        xbmc.log("[plugin.video.hotstar-rain-%s]: %s" %(addon_version, string))

def make_request(url):
    try:
		print 'enableip is', enableip
		if enableip=='true':
			headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch', 'Connection':'keep-alive', 'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)', 'X-Forwarded-For': ipaddress}
		else:
			headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch', 'Connection':'keep-alive', 'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)'}
		# print 'url to fetch', url
		print 'headers are', headers
		response = s.get(url, headers=headers, cookies=s.cookies, verify=False)
		data = response.text
		return data
    except urllib2.URLError, e:    # This is the correct syntax
        print e
        ##sys.exit(1)

def new_menu():
	addDir(21, 'Featured (on main page)', 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId=5637&channel=PCTV','', '')
	addDir(3, '[B][COLOR orange]Movies[/COLOR][/B]', '', '','')
	addDir(2, '[B][COLOR white]TV Shows[/COLOR][/B]', '', '','')
	addDir(5, '[B][COLOR green]Movie Collections[/COLOR][/B]', '','', '')
	addDir(24, '[B]Sports[/B]', '', '','')
	addDir(31, '[B][COLOR yellow]TV Channels[/COLOR][/B]','','','')
	addDir(12, '[B]Search[/B]', '', '','')
	# addDir(30, '[B][COLOR red]Old look (deprecated)[/COLOR][/B]', '','', '')
	
def get_menu():
	addDir(3, '[B][COLOR orange]Movies[/COLOR](old look)[/B]', '', '','')        
	addDir(2, '[B][COLOR white]TV Shows[/COLOR](old look)[/B]', '', '','')
	addDir(5, '[B][COLOR green]Movie Collections[/COLOR](old look)[/B]', '','', '')	
	addDir(4, '[B]Sports[/B](old look)', '','', '')	

def get_main_featured():
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentList']:
		title = '[COLOR orange]'+result['contentTitle'].encode('ascii', 'ignore')+'[/COLOR] '
		duration = result['duration']
		episode = '[COLOR green]'+result['episodeTitle'].encode('ascii', 'ignore')+'[/COLOR]'
		show_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&type=VOD&id='+str(result['contentId'])
		show_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-vl.jpg'
		addDir(9, title+' - '+episode, show_link, show_img,duration, fold)
	
	# setView('episodes', 'episode-view')
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def get_channels():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&appVersion=5.0.21&categoryId=564&channel=PCTV')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList'][0]['categoryList']:
			title = '[B][COLOR orange]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B]'
			channel_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
			channel_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-vl.jpg'
			addDir(32, title, channel_link, channel_img, False)
			
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
			
def get_channel_shows():
	html = make_request(url)
	data=html
	html=json.loads(data)
	for result in html['resultObj']['contentList']:
			title = '[B][COLOR orange]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B]'
			season_link = 'http://account.hotstar.com/AVS/besc?action=GetAggregatedContentDetails&channel=PCTV&contentId='+str(result['contentId'])
			show_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-vl.jpg'
			addDir(6, title, season_link, show_img, False)
			
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)		
	
def get_tvshows():
	html = make_request('http://search.hotstar.com/AVS/besc?action=SearchContents&channel=PCTV&moreFilters=type:SERIES%3Blanguage:'+language+'%3B&query=*')
	#data = html.decode('utf-8')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['response']['docs']:
		title = '[B][COLOR orange]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B]'
		season_link = 'http://account.hotstar.com/AVS/besc?action=GetAggregatedContentDetails&channel=PCTV&contentId='+str(result['contentId'])
		show_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-vl.jpg'
		addDir(6, title, season_link, show_img, False)
		
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def get_movies():
	if url:
		print 'url is: ', url
		base_url = url
		index = re.compile('Index=(\d*)').findall(str(base_url))[0]
	else:
		index = 0
		base_url = 'http://search.hotstar.com/AVS/besc?action=SearchContents&channel=PCTV&maxResult='+perpage+'&moreFilters=language:'+language+'&query=*&searchOrder='+moviessortType+'&startIndex='+str(index)+'&type=MOVIE'
		print 'base_url is:', base_url
		
	html = make_request(base_url)
	data = html
	html = json.loads(data)
	total = html['resultObj']['response']['numFound']
	for result in html['resultObj']['response']['docs']:
		title = '[B][COLOR orange]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B]'
		duration = result['duration']
		movie_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&type=VOD&id='+str(result['contentId'])
		movie_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+result['urlPictures']+'/PCTV-'+result['urlPictures']+'-vl.jpg'
		addDir(9,title, movie_link, movie_img,duration, fold)
	index_page = int(index)+int(perpage)
	if (index_page<int(total)+1):
		index = index_page
		next = 'http://search.hotstar.com/AVS/besc?action=SearchContents&channel=PCTV&maxResult='+perpage+'&moreFilters=language:'+language+'&query=*&searchOrder='+moviessortType+'&startIndex='+str(index)+'&type=MOVIE'
		addDir(3, '>>> Next Page >>>', next, '')
		
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

def get_sports():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=1678&channel=PCTV')
	data = html
	html = json.loads(data)
	title = '[B]Featured[/B]  [COLOR red][Live - if showing][/COLOR]'
	sports_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId=5891&channel=PCTV'
	addDir(14, title, sports_link, '', False)
	for result in html['resultObj']['categoryList'][0]['categoryList']:
		title = result['categoryName']
		sports_link = 'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='+str(result['categoryId'])+'&channel=PCTV'
		sports_img = ''#'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hs.jpg'
		addDir(13, title, sports_link, sports_img, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
		
def get_new_sports():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=5962&channel=PCTV')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList'][0]['categoryList']:
		if '5967' not in str(result['categoryId']):
			if 'Popular in' not in result['contentTitle']:
				if 'masthead' in result['contentTitle']:
					title = '[B][COLOR red]Live Events[/COLOR][/B] (if showing)'
				else:
					title = result['contentTitle']
				sports_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
				sports_img = ''
				addDir(14, title, sports_link, sports_img, False)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)		
		
def get_ss():
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList'][0]['categoryList']:
		title = result['contentTitle']
		if result['categoryType']=='TYPE_NODE':
			ss_link = 'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='+str(result['categoryId'])+'&channel=PCTV'
		else:
			ss_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
		ss_img = ''
		addDir(14, title, ss_link, ss_img, False)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
def get_ss_event():
	# print 'ss url', url
	html = make_request(url)
	data = html
	html = json.loads(data)
	if 'ArrayContent' in url:
		for result in html['resultObj']['contentList']:
			title = result['contentTitle']
			duration = result['duration']
			event_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id='+str(result['contentId'])+'&type=VOD'
			event_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hl.jpg'
			addDir(9, title, event_link, event_img,duration, fold)
	else:
		for result in html['resultObj']['categoryList'][0]['categoryList']:
			title = result['contentTitle']
			event_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
			event_img = ''
			addDir(14, title, event_link, event_img, False)
	
	setView('episodes', 'episode-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def get_collections():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=558&channel=PCTV')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList']:
		for subval in result['categoryList']:
			if language in subval['language'].lower():
				title = '[B][COLOR green]'+subval['categoryName']+'[/COLOR][/B]'
				col_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(subval['categoryId'])+'&channel=PCTV'
				col_img='http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hs.jpg'
				addDir(10, title, col_link, col_img, False)

	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
				
def col_movies():
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentList']:
		title = '[B][COLOR orange]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B]'
		duration = result['duration']
		colm_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&type=VOD&id='+str(result['contentId'])
		colm_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+result['urlPictures']+'/PCTV-'+result['urlPictures']+'-vl.jpg'
		addDir(9, title, colm_link, colm_img,duration, fold)
		
	setView('movies', 'movie-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
		
def get_search():
    if url:
	    search_url = url
    else:
        keyb = xbmc.Keyboard('', 'Search for Movies/TV Shows/Trailers/Videos in all languages')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search_term = urllib.quote_plus(keyb.getText())
            if not search_term:
                addon.show_ok_dialog(['empty search not allowed'.title()], addon.get_name())
                sys.exit()			
        else:
            sys.exit()			
			
        search_url = 'http://search.hotstar.com/AVS/besc?action=SearchContents&channel=PCTV&facets=type%3Blanguage%3Bgenre&maxResult=34&query='+str(search_term)+'&startIndex=0&type=MOVIE,SERIES,SPORT,SPORT_LIVE'
	
    html = make_request(search_url)
    data = html
    html = json.loads(data)
    for result in html['resultObj']['response']['docs']:
		title = '[B][COLOR blue]'+result['contentTitle'].encode('ascii','ignore')+'[/COLOR][/B] - '+result['language']
		duration = result['duration']
		search_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&type=VOD&id='+str(result['contentId'])
		search_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+result['urlPictures']+'/PCTV-'+result['urlPictures']+'-vl.jpg'
		addDir(9, title, search_link, search_img,duration, fold)
		
    setView('movies', 'movie-view')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
    			
    		
def get_seasons():
	#print url
	html = make_request(url)
	#print html
	#data = html.decode('utf-8')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentInfo']:
		seasons = result['contentTitle']
		season_link = 'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='+str(result['categoryId'])+'&channel=PCTV'#'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='++'&channel=PCTV'#			
		season_img = ''#'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hcc.jpg'
		addDir(7, seasons, season_link, season_img, False)
			
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
		
def get_seasons_ep_links():
	print "get seasons ep links: "+url
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList']:
		for result2 in result['categoryList']:
			ep_titles = result2['categoryName']
			ep_links = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result2['categoryId'])+'&channel=PCTV'
			# ep_links = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&appVersion=5.0.15&categoryId=423&channel=PCTV'
			ep_images = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result2['urlPictures'])[-2:]+'/'+str(result2['urlPictures'])+'/PCTV-'+str(result2['urlPictures'])+'-hsea.jpg'
			addDir(8, ep_titles, ep_links, ep_images, False)
		
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('episodes', 'episode-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)	
	
def get_episodes():
	print "get_episodes: "+url
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentList']:
		fin_ep_titles = '[B][COLOR orange]'+str(result['episodeNumber'])+' - '+result['episodeTitle'].encode('ascii', 'ignore')+'[/COLOR][/B]'
		duration = result['duration']
		fin_ep_links = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id='+str(result['contentId'])+'&type=VOD'
		fin_ep_images = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hs.jpg'
		addDir(9, fin_ep_titles, fin_ep_links, fin_ep_images,duration, fold)
		
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('episodes', 'episode-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def get_video_url():
    videos = []
    params = []
    html = make_request(url)
    data = html
    html = json.loads(data)
    manifest1 = html['resultObj']['src']
    manifest1 = manifest1.replace('http://','https://')
    manifest1 = manifest1.replace('/z/','/i/')
    manifest1 = manifest1.replace('manifest.f4m', 'master.m3u8')
    if (quality=='highest'):
		manifest2 = manifest1.replace('1300,2000', '3000,4500')
		manifest_url = make_request(manifest2)
		# print manifest_url
		if 'EXTM3U' in manifest_url:
			matchlist2 = re.compile("BANDWIDTH=([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
			manifest1 = None
			if matchlist2:
				for (size, video) in matchlist2:
					if size:
						size = int(size)
					else:
						size = 0
					videos.append( [size, video] )
		else:
			manifest1 = manifest2.replace('3000,4500', '1300,2000')
    
    if manifest1:
		manifest_url = make_request(manifest1)
		print manifest_url
		if manifest_url:
			if (quality=='highest' or quality=='let me choose'):
				# matchlist2 = re.compile("BANDWIDTH=([0-9]+).*RESOLUTION[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
				matchlist2 = re.compile("RESOLUTION=\d+x([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
			elif (quality == '720p'):
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x720[^\n]*\n([^n].*)").findall(str(manifest_url))
			elif (quality == '404p'):
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x404[^\n]*\n([^n].*)").findall(str(manifest_url))
			else:
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x360[^\n]*\n([^n].*)").findall(str(manifest_url))
			if matchlist2:
				for (size, video) in matchlist2:
					if size:
						size = int(size)
					else:
						size = 0
					videos.append( [size, video] )
		else:
			videos.append( [-2, match] )
    
    videos.sort(key=lambda L : L and L[0], reverse=True)
    cookieString = ""
    c = s.cookies
    i = c.items()
    for name2, value in i:
		cookieString+= name2 + "=" + value + ";"
    # print 'cookieString is', cookieString
	
    if (quality == 'let me choose'):
		print videos
		for video in videos:
			size = '(' + str(video[0]) + 'p) '
			if enableip=='true':
				if 'index_1364_av' in video[1]:
					old_size = size
					size = '(720p) '
					old_vid = video[1]
					new_vid = video[1].replace('index_1364_av', 'index_2064_av')
					addDir(0, size + name, new_vid+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress, image, isplayable=True)
					addDir(0, old_size + name, old_vid+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress, image, isplayable=True)
				else:
					addDir(0, size + name, video[1]+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress, image, isplayable=True)
			else:
				if 'index_1364_av' in video[1]:
					old_size = size
					size = '[COLOR green][720p][/COLOR] '
					old_vid = video[1]
					new_vid = video[1].replace('index_1364_av', 'index_2064_av')
					addDir(0, size + name, new_vid+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress, image, isplayable=True)
					addDir(0, old_size + name, old_vid+"|Cookie="+cookieString, image, isplayable=True)
				else:
					addDir(0, size + name, video[1]+"|Cookie="+cookieString, image, isplayable=True)
    else:
		if videos:
			raw3_start = videos[0][1]
			if enableip=='true':
				high_video = raw3_start+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress
			else:
				high_video = raw3_start+"|Cookie="+cookieString
			print 'high_video is: ',high_video
			listitem =xbmcgui.ListItem(name)
			listitem.setPath(high_video)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		else:
			movie_id = 'IP issue?'
			dialog.notification("No Video Links available", movie_id, xbmcgui.NOTIFICATION_INFO, 4000)

    setView('movies', 'movie-view')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)	
		
def setView(content, viewType):
        
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )		
		
def addDir(mode,name,url,image,duration="",isplayable=False):
	name = name.encode('utf-8', 'ignore')
	url = url.encode('utf-8', 'ignore')

	if 0==mode:
		link = url
		print link
	else:
		link = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&image="+urllib.quote_plus(image)

	ok=True
	item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
	item.addStreamInfo('video', {'codec': 'h264'})
	item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
	if 9==mode:
		if '[' in name:
			name = urllib.unquote_plus(name).split(']')[2].split('[')[0]
	item.setInfo( type="Video", infoLabels={ "OriginalTitle": name, "Duration": duration } )
	# print 'printing item', item
	if 'vl.jpg' in image:
		image2 = image.replace('vl.jpg', 'hl.jpg')
		item.setArt({'fanart': image2})
	else:
		item.setArt({'fanart': image})
	isfolder=True
	if isplayable:
		item.setProperty('IsPlayable', 'true')
		isfolder=False
		# if (quality == 'let me choose'):
			# name = urllib.unquote_plus(name).split(") ")[1]
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=link,listitem=item,isFolder=isfolder)
	return ok
	
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()	
mode=None
name=None
url=None
image=None

try:
    mode=int(params["mode"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    image=urllib.unquote_plus(params["image"])
except:
    pass
	
if mode==None:
	new_menu()
    
if mode==30:
	get_menu()
	
if mode==2:
    get_tvshows()

if mode==3:
    get_movies()
    
if mode==4:
    get_sports()
	
if mode==13:
	get_ss()
	
if mode==14:
	get_ss_event()
	
if mode==5:
	get_collections()
	
if mode ==10:
	col_movies()

if mode==6:
    get_seasons()

if mode==7:
    get_seasons_ep_links()

if mode==8:
    get_episodes()
    
if mode==9:
    get_video_url()
	
if mode==12:
	get_search()
	
if mode==21:
	get_main_featured()
	
if mode==24:
	get_new_sports()
	
if mode==31:
	get_channels()

if mode==32:
	get_channel_shows()

s.close()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))