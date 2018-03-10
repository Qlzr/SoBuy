from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserForm
from .models import User
import pymysql
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