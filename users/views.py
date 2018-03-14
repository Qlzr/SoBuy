from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserForm
from .models import User, Collention
import pymysql
from django.utils import timezone

# Create your views here.
def register(request):

	redirect_to = request.POST.get('next', request.GET.get('next', ''))
	#只有当请求为POST时，才表示用户提交了注册信息
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			form.save()

			if redirect_to:
				return redirect(redirect_to)
			else:
				return redirect('/')

	else:
		#请求不是POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
		form = RegisterForm()

	#渲染模板
	#如果用户正在访问注册页面，则渲染的是一个空的注册表单
	#如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
	return render(request, 'users/register.html', context={'form': form, 'next':redirect_to})

def personal(request):
	return render(request, 'users/personal.html')

#收藏商品功能
def collect_commodity(request):
	collect = Collention.objects.create(
		user = request.GET.get('user', ''), 
		name = request.GET.get('name', ''),
		price = request.GET.get('price', ''),
		detail_url = request.GET.get('detail_url', ''),
		img_url = request.GET.get('img_url', ''),
		website = request.GET.get('website', ''),
		collect_time = timezone.now())
	collect.save()
	return render(request, 'users/collect_success.html')

#展示收藏夹
def collentions(request, user):
	collentions = Collention.objects.filter(user=user).order_by('-collect_time')
	if len(collentions) == 0:
		collect_empty = True
	else:
		collect_empty = False
	context = {'collentions': collentions, 'collect_empty': collect_empty}
	return render(request, 'users/collentions.html', context=context)

#删除收藏品
def delete_collention(request, pk):
	d = Collention.objects.get(pk=pk)
	d.delete()
	return render(request, 'users/delete_collention.html')

def change_user(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('/')

	else:
		#请求不是POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
		form = UserForm(instance=request.user)

	#渲染模板
	#如果用户正在访问注册页面，则渲染的是一个空的注册表单
	#如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
	return render(request, 'users/change_user.html', context={'form': form})
