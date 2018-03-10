from django.shortcuts import render
from .form import KeywordForm
from django.utils import timezone
from .crawler import get_all_com, first_get_com
from .models import Commodity
from django.http import HttpResponse

def index(request):
	form = KeywordForm()
	username = request.COOKIES.get('cookie_username', '')
	context = {'form': form, 'username': username}
	return render(request, 'search/index.html', context=context)

def search_commodity(request):
	if request.method == 'POST':
		form = KeywordForm(request.POST)
		user = request.POST.get('user', '')

		# 检查表单数据的合法性
		if form.is_valid():
			k = form.save(commit=False)
			k.created_time = timezone.now()
			k.user = user
			k.save()

			#爬虫爬取商品
			data = first_get_com(k.word)
			com_list = data['com_list']
			page_count = data['page_count']
			jd_page_count = data['jd_page_count']
			dd_page_count = data['dd_page_count']
			keyword = k.word
			form_r = KeywordForm()
			username = request.COOKIES.get('cookie_username', '')
			current_page = 1
			if page_count < 5:
				page = [x for x in range(2, page_count+1)]
			else:
				page = [x for x in range(2,6)]
			context={
			'com_list':com_list, 
			'form':form_r, 
			'keyword': keyword, 
			'current_page': current_page, 
			'page':page,
			'page_count': page_count,
			'jd_page_count':jd_page_count,
			'dd_page_count':dd_page_count
			}
			return render(request, 'search/search.html', context=context)
	else:
		return render(request, 'search/formerror.html')

def search_page(request, keyword, page):
	page_count = int(request.GET.get('page_count', ''))
	jd_page_count = int(request.GET.get('jd_page_count', ''))
	dd_page_count = int(request.GET.get('dd_page_count', ''))
	page = int(page)
	com_list = get_all_com(keyword, page, page_count, jd_page_count, dd_page_count)
	form = KeywordForm()
	current_page = page
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
	}
	return render(request, 'search/search.html', context=context)