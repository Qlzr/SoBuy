import requests
import urllib
from bs4 import BeautifulSoup
import random
import threading

#首次请求
def search_first(keyword):
	com_list_jd,jd_page_count = first_get_jd(keyword)
	com_list_dd,dd_page_count = first_get_dd(keyword)
	page_count = max(jd_page_count, dd_page_count)
	current_page = 1
	befor_page,after_page = resolve_page(current_page, page_count)
	com_list = com_list_jd + com_list_dd
	if len(com_list) == 0:
		search_empty = True
	else:
		search_empty = False
	random.shuffle(com_list)
	data = {
		'com_list': com_list,
		'current_page': current_page,
		'befor_page': befor_page,
		'after_page': after_page,
		'jd_page_count': jd_page_count,
		'dd_page_count': dd_page_count,
		'page_count': page_count,
		'search_empty':search_empty,
		'website': '1',
		'sort': '1',
	}
	return data

def first_get_jd(keyword):
	key = urllib.parse.quote(keyword)
	url = 'https://search.jd.com/Search?keyword='+ key +'&enc=utf-8&wq=' + key
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
	r = requests.get(url=url, headers=headers)
	r.encoding = 'utf-8'
	html = r.text
	soup = BeautifulSoup(html, 'lxml')
	jd_page_count = soup.find(class_='fp-text').i.get_text()
	jd_page_count = int(jd_page_count) * 2
	commodity_list = soup.find_all(name='li',class_='gl-item')
	com_list = resolve_jd(commodity_list)
	if 0< len(com_list) < 30:
		jd_page_count = jd_page_count - 1
	return (com_list, jd_page_count)

def first_get_dd(keyword):
	key = urllib.parse.quote(keyword)
	url = 'http://search.dangdang.com/?key='+ key +'&act=input&show=big&show_shop=0#J_tab'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'} 
	response = requests.get(url=url, headers=headers)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	dd_page_count = soup.find(class_='data').find_all(name='span')[1].get_text()[1:]
	dd_page_count = int(dd_page_count) * 2
	commodity = soup.find(dd_name="普通商品区域").find_all(name='li')
	com_list = resolve_dd(commodity[:30])
	if 0 < len(com_list) < 30:
		dd_page_count = dd_page_count - 1
	return (com_list,dd_page_count)


#汇总综合排序的商品信息
def get_all_com(keyword, page, page_count, jd_page_count, dd_page_count):
	if page > page_count:
		com_list_jd = []
		com_list_dd = []
	elif jd_page_count < page < page_count:
		com_list_jd = []
		com_list_dd = get_dd(keyword, page)
	elif dd_page_count < page < page_count:
		com_list_jd = get_jd(keyword, page, 1)
		com_list_dd = []
	else:
		com_list_jd = get_jd(keyword, page, 1)
		com_list_dd = get_dd(keyword, page)
	com_list = com_list_jd + com_list_dd
	random.shuffle(com_list)
	return com_list

#获取半页京东的商品信息
def get_jd(keyword, page, sort=1):
	key = urllib.parse.quote(keyword)
	if int(page) % 2 == 0:
		para = '&scrolling=y'
	else:
		para = ''
	if sort == 1:
		url = 'https://search.jd.com/s_new.php?keyword='+ key +'&enc=utf-8&&qrst=1&rt=1&stop=1&vt=2&wq='+ key +'&page='+ str(page) +'&s='+str((int(page)-1)*30+1) + para
	elif sort == 2:
		url = 'https://search.jd.com/s_new.php?keyword='+ key +'&enc=utf-8&&qrst=1&rt=1&stop=1&vt=2&wq='+ key +'&page='+ str(page) +'&s='+str((int(page)-1)*30+1) + '&psort=2' + para
	else:
		url = 'https://search.jd.com/s_new.php?keyword='+ key +'&enc=utf-8&&qrst=1&rt=1&stop=1&vt=2&wq='+ key +'&page='+ str(page) +'&s='+str((int(page)-1)*30+1) + '&psort=1' + para
	headers = {
		'Host': 'search.jd.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
		'Referer': 'https://search.jd.com/Search?keyword='+ key +'&enc=utf-8',
		'X-Requested-With': 'XMLHttpRequest'
		}
	try:
		r = requests.get(url=url, headers=headers)
		r.encoding = 'utf-8'
		html = r.text
		soup = BeautifulSoup(html, 'lxml')
		commodity_list = soup.find_all(name='li',class_='gl-item')
		com_list = resolve_jd(commodity_list)
		return com_list
	except:
		return []

#获取半页的商品信息
def get_dd(keyword, page):
	key = urllib.parse.quote(keyword)
	url = 'http://search.dangdang.com/?key='+ key +'&act=input&page_index='+str((int(page)+1) // 2) +'&show=big&show_shop=0#J_tab'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
	try:
		response = requests.get(url=url, headers=headers)
		html = response.text
		soup = BeautifulSoup(html, 'lxml')
		commodity = soup.find(dd_name="普通商品区域").find_all(name='li')
		if int(page) % 2 == 1:
			i = 0
			j = 30
		else:
			i = 30
			j = 60
		com_list = resolve_dd(commodity[i:j])
		return com_list
	except:
		return []


#解析京东页面的商品信息
def resolve_jd(commodity_list):
	com_list = []
	for com in commodity_list:
		com_info = {}
		com_info['name'] = com.find(class_='p-name').a.em.get_text().strip()
		com_info['price'] = com.find(class_='p-price').find(name='i').get_text()
		try:
			com_info['price'] = com.find(class_='p-price').strong.attrs['data-price']
		except:
			com_info['price'] = com.find(class_='p-price').find(name='i').get_text()
		img_attrs = com.find(name='img', class_='err-product').attrs
		if 'data-lazy-img' in img_attrs:
			com_info['img_url'] = 'http:' + img_attrs['data-lazy-img']
		else:
			com_info['img_url'] = 'http:' + img_attrs['src']
		com_info['detail_url'] = 'https:' + com.find(class_='p-name').a.attrs['href'].replace('https://', '//')
		com_info['website'] = '京东'
		com_list.append(com_info)
	return com_list

#解析当当页面的商品信息
def resolve_dd(commodity_list):
	com_list = []
	for com in commodity_list:
		com_info = {}
		com_info["name"] = com.find(class_='name').get_text().strip()
		com_info["price"] = com.find(class_='price_n').get_text().strip()[1:]
		com_info['detail_url'] = com.find(class_='name').a.attrs['href']
		img_attrs = com.find(class_='pic').img.attrs
		if 'data-original' in img_attrs:
			com_info['img_url'] = img_attrs['data-original']
		else:
			com_info['img_url'] = img_attrs['src']
		com_info['website'] = '当当'
		com_list.append(com_info)
	return com_list

#生成前页和后页
def resolve_page(current_page, page_count):
	if page_count < 5:
		befor_page = [x for x in range(1, current_page)]
		after_page = [x for x in range(current_page + 1, page_count + 1)]
	elif page_count >5 and page_count - current_page < 2 :
		befor_page = [x for x in range(current_page - (4 - (page_count - current_page)), current_page)]
		after_page = [x for x in range(current_page + 1, page_count + 1)]
	elif page_count >5 and current_page - 1 < 2:
		befor_page = [x for x in range(1, current_page)]
		after_page = [x for x in range(current_page + 1, current_page + (5 - (current_page - 1)))]
	else:
		befor_page = [x for x in range(current_page - 2, current_page)]
		after_page = [x for x in range(current_page + 1, current_page + 3)]
	return (befor_page,after_page)


#首次获取京东商品信息
def search_jd_first(keyword, sort):
	key = urllib.parse.quote(keyword)
	if sort == 1:
		url = 'https://search.jd.com/Search?keyword='+ key +'&enc=utf-8&wq=' + key
	elif sort == 2:
		url = 'https://search.jd.com/Search?keyword='+ key +'&enc=utf-8&wq=' + key +'&psort=2'
	else:
		url = 'https://search.jd.com/Search?keyword='+ key +'&enc=utf-8&wq=' + key +'&psort=1'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
	r = requests.get(url=url, headers=headers)
	r.encoding = 'utf-8'
	html = r.text
	soup = BeautifulSoup(html, 'lxml')
	page_count = int(soup.find(class_='fp-text').i.get_text())
	commodity_list = soup.find_all(name='li',class_='gl-item')
	com_list = resolve_jd(commodity_list)
	if len(com_list) == 0:
		search_empty = True
	elif len(com_list) == 30:
		com_list = com_list + get_jd(keyword, 2, sort)
		search_empty = False
	else:
		search_empty = False
	current_page = 1
	befor_page,after_page = resolve_page(current_page, page_count)
	data = {
		'com_list': com_list,
		'current_page': current_page,
		'befor_page': befor_page,
		'after_page': after_page,
		'page_count': page_count,
		'search_empty': search_empty,
		'website': '2',
		'sort': str(sort),
	}
	return data

#获取当当整页商品信息
def search_dd(keyword, page, sort):
	key = urllib.parse.quote(keyword)
	if sort == 1:
		url = 'http://search.dangdang.com/?key='+ key +'&act=input&show=big&show_shop=0&page_index='+ str(page)
	elif sort == 2:
		url = 'http://search.dangdang.com/?key='+ key +'&SearchFromTop=1&catalog=&show=big&show_shop=0&page_index='+ str(page) +'&sort_type=sort_xlowprice_asc'
	else:
		url = 'http://search.dangdang.com/?key='+ key +'&SearchFromTop=1&catalog=&show=big&show_shop=0&page_index='+ str(page) +'&sort_type=sort_xlowprice_desc'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'} 
	response = requests.get(url=url, headers=headers)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	page_count = int(soup.find(class_='data').find_all(name='span')[1].get_text()[1:])
	commodity = soup.find(dd_name="普通商品区域").find_all(name='li')
	com_list = resolve_dd(commodity)
	if len(com_list) == 0:
		search_empty = True
	else:
		search_empty = False
	current_page = 1
	befor_page, after_page = resolve_page(current_page, page_count)
	data = {
		'com_list': com_list,
		'current_page': current_page,
		'befor_page': befor_page,
		'after_page': after_page,
		'page_count': page_count,
		'search_empty': search_empty,
		'website': '3',
		'sort': str(sort),
	}
	return data

#首次条件搜索获取商品信息
def select_first(keyword, website, sort):
	if (website == '1') & (sort == '1'): 
		data = search_first(keyword)
	elif (website == '2'):
		data = search_jd_first(keyword, int(sort))
	elif (website == '3'):
		data = search_dd(keyword, 1, int(sort))
	else:
		pass
	return data

#条件搜索的翻页
def select_pages(keyword, page, page_count, website, sort):
	if 0 < page <= page_count:
		if website == '2':
			com_list = get_jd(keyword, page*2-1, int(sort))
			if len(com_list) == 0:
				search_empty = True
			elif len(com_list) == 30:
				com_list = com_list + get_jd(keyword, page*2, int(sort))
				search_empty = False
			else:
				search_empty = False
		else:
			com_list = search_dd(keyword, page, int(sort))
			if len(com_list) == 0:
				search_empty = True
			else:
				search_empty = False
	else:
		com_list = []
		search_empty = True
	befor_page,after_page = resolve_page(page, page_count)
	data = {
		'com_list': com_list,
		'current_page': page,
		'befor_page': befor_page,
		'after_page': after_page,
		'page_count': page_count,
		'search_empty': search_empty,
	}
	return data