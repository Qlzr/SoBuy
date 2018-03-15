from django.shortcuts import render
from .form import KeywordForm, SelectForm
from django.utils import timezone
from .crawler import get_all_com, search_first, select_first, select_pages, resolve_page
from django.http import HttpResponse

#获取首页
def index(request):
	form = KeywordForm()
	username = request.COOKIES.get('cookie_username', '')
	context = {'form': form, 'username': username}
	return render(request, 'search/index.html', context=context)

#根据关键词搜索商品
def search_commodity(request):
	user = request.GET.get('user', '')
	select_form = SelectForm()
	if request.method == 'POST':
		form = KeywordForm(request.POST)

		# 检查表单数据的合法性
		if form.is_valid():
			k = form.save(commit=False)
			k.created_time = timezone.now()
			k.user = user
			k.save()

			#爬虫爬取商品
			data = search_first(k.word)
			keyword = k.word
			form_r = KeywordForm()
			context={
				'com_list': data['com_list'], 
				'form': form_r, 
				'keyword': keyword, 
				'current_page': data['current_page'], 
				'befor_page': data['befor_page'],
				'after_page': data['after_page'],
				'page_count': data['page_count'],
				'jd_page_count': data['jd_page_count'],
				'dd_page_count': data['dd_page_count'],
				'select_form': select_form,
				'search_empty': data['search_empty'],
				'website': data['website'],
				'sort': data['sort'],
				}
			return render(request, 'search/search.html', context=context)
	else:
		return render(request, 'search/formerror.html')


#全部网站综合排序翻页功能
def search_page(request, keyword, page):
	select_form = SelectForm()
	page_count = int(request.GET.get('page_count', ''))
	jd_page_count = int(request.GET.get('jd_page_count', ''))
	dd_page_count = int(request.GET.get('dd_page_count', ''))
	page = int(page)
	com_list = get_all_com(keyword, page, page_count, jd_page_count, dd_page_count)
	form = KeywordForm()
	current_page = page
	befor_page,after_page = resolve_page(page, page_count)
	if len(com_list) == 0:
		search_empty = True
	else:
		search_empty = False
	context={
	'com_list': com_list, 
	'keyword': keyword, 
	'form': form, 
	'current_page': current_page,
	'befor_page':befor_page,
	'after_page':after_page,
	'page_count': page_count,
	'jd_page_count':jd_page_count,
	'dd_page_count':dd_page_count,
	'search_empty':search_empty,
	'select_form':select_form,
	'website': '1',
	'sort': '1',
	}
	return render(request, 'search/search.html', context=context)

#筛选商品（条件搜索）
def select_commodity(request, keyword):
	if request.method == 'POST':
		select_form = SelectForm(request.POST, request.FILES)
		form = KeywordForm()
		if select_form.is_valid():
			condition = select_form.clean()
			#获取数据
			data = select_first(keyword, condition['website'], condition['sort'])
			if (condition['website'] == '1') & (condition['sort'] == '1'):
				context={
				'com_list': data['com_list'], 
				'form': form, 
				'keyword': keyword, 
				'current_page': data['current_page'], 
				'befor_page': data['befor_page'],
				'after_page': data['after_page'],
				'page_count': data['page_count'],
				'jd_page_count': data['jd_page_count'],
				'dd_page_count': data['dd_page_count'],
				'select_form': select_form,
				'search_empty': data['search_empty'],
				'website': data['website'],
				'sort': data['sort'],
				}
			else:
				context={
				'com_list': data['com_list'], 
				'form': form, 
				'keyword': keyword, 
				'current_page': data['current_page'], 
				'befor_page': data['befor_page'],
				'after_page': data['after_page'],
				'page_count': data['page_count'],
				'select_form': select_form,
				'search_empty': data['search_empty'],
				'website': data['website'],
				'sort': data['sort'],
				}
			return render(request, 'search/search.html', context=context)
	else:
		return render(request, 'search/formerror.html')


#条件搜索的翻页
def select_page(request, keyword, page):
	form = KeywordForm()
	website = request.GET.get('website', '')
	sort = request.GET.get('sort', '')
	page_count = int(request.GET.get('page_count',''))
	select_form = SelectForm({'website': website, 'sort': sort})
	data = select_pages(keyword, int(page), page_count, website, sort)
	context={
		'com_list': data['com_list'], 
		'form': form, 
		'keyword': keyword, 
		'current_page': int(page), 
		'befor_page': data['befor_page'],
		'after_page': data['after_page'],
		'page_count': page_count,
		'select_form': select_form,
		'search_empty': data['search_empty'],
		'website': website,
		'sort': sort,
	}
	return render(request, 'search/search.html', context=context)