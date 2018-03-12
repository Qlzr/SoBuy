import requests
import urllib
from bs4 import BeautifulSoup
import random

#汇总爬取到的商品信息
def get_all_com(keyword, page, page_count, jd_page_count, dd_page_count):
	if page > page_count:
		com_list_jd = []
		com_list_dd = []
	elif jd_page_count < page < page_count:
		com_list_jd = []
		com_list_dd = get_dd(keyword, page)
	elif dd_page_count < page < page_count:
		com_list_jd = get_jd(keyword, page)
		com_list_dd = []
	else:
		com_list_jd = get_jd(keyword, page)
		com_list_dd = get_dd(keyword, page)
	com_list = com_list_jd + com_list_dd
	random.shuffle(com_list)
	return com_list

#获取京东的商品信息
def get_jd(keyword, page):
	key = urllib.parse.quote(keyword)
	if int(page) % 2 == 0:
		para = '&scrolling=y'
	else:
		para = ''
	url = 'https://search.jd.com/s_new.php?keyword='+ key +'&enc=utf-8&&qrst=1&rt=1&stop=1&vt=2&wq='+ key +'&page=2&s='+str((int(page)-1)*30+1) + para
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
		com_list = []
		for com in commodity_list:
			com_info = {}
			com_info['name'] = com.find(class_='p-name').a.em.get_text().strip()
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
	except:
		return []

#获取当当网的商品信息
def get_dd(keyword, page):
	key = urllib.parse.quote(keyword)
	url = 'http://search.dangdang.com/?key='+ key +'&act=input&page_index='+str((int(page)+1) // 2) +'&show=big&show_shop=0#J_tab'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
	try:
		response = requests.get(url=url, headers=headers)
		html = response.text
		soup = BeautifulSoup(html, 'lxml')
		commodity_info = []
		commodity = soup.find(dd_name="普通商品区域").find_all(name='li')
		if int(page) % 2 == 1:
			i = 0
			j = 30
		else:
			i = 30
			j = 60
		for com in commodity[i:j]:
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
			commodity_info.append(com_info)
		return commodity_info
	except:
		return []

#首次请求
def first_get_com(keyword):
	com_list_jd,jd_page_count = first_get_jd(keyword)
	com_list_dd,dd_page_count = first_get_dd(keyword)
	page_count = max(jd_page_count, dd_page_count)
	com_list = com_list_jd + com_list_dd
	random.shuffle(com_list)
	data = {
		'com_list': com_list,
		'jd_page_count': jd_page_count,
		'dd_page_count': dd_page_count,
		'page_count': page_count,
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
	com_list = []
	for com in commodity_list:
		com_info = {}
		com_info['name'] = com.find(class_='p-name').a.em.get_text().strip()
		com_info['price'] = com.find(class_='p-price').find(name='i').get_text()
		img_attrs = com.find(name='img', class_='err-product').attrs
		if 'data-lazy-img' in img_attrs:
			com_info['img_url'] = 'http:' + img_attrs['data-lazy-img']
		else:
			com_info['img_url'] = 'http:' + img_attrs['src']
		com_info['detail_url'] = 'https:' + com.find(class_='p-name').a.attrs['href'].replace('https://', '//')
		com_info['website'] = '京东'
		com_list.append(com_info)
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
	commodity_info = []
	commodity = soup.find(dd_name="普通商品区域").find_all(name='li')
	for com in commodity[:30]:
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
		commodity_info.append(com_info)
	if 0 < len(commodity_info) < 30:
		dd_page_count = dd_page_count - 1
	return (commodity_info,dd_page_count)

