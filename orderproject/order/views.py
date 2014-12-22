from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from order.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

	menu_list = Menu.objects.order_by("price")
	paginator = Paginator(menu_list,5)

	page = request.GET.get('page')
	try:
		menus = paginator.page(page)
	except PageNotAnInteger:
		menus = paginator.page(1)
	except EmptyPage:
		menus = paginator.page(paginator.num_pages)

	return render(request, 'index.html', { "menus" : menus })

def detail(request, menu_id):

	menu = get_object_or_404(Menu, id=menu_id)
	context = {
		'menu' : menu
	}

	return render(request, 'detail.html',context)
@login_required
def buy(request, menu_id):
		quantity = list(range(1,11))
		menu = get_object_or_404(Menu, id=menu_id)

		context = {
			'menu' : menu,
			'menu_id' : menu_id,
			'quantity' : quantity
		}

		return render(request, 'buy.html',context)

def buy_submit(request, menu_id):
	
	if request.method == 'GET':
		context = {
			'error_message' : "비정상적인 접근입니다",
		}
		return render(request, "pay.html", context)

	elif request.method == 'POST' :
		try :
			order_quantity = request.POST['order_quantity']
			order_address = request.POST['order_address']
			order_phone = request.POST['order_phone']

			if len(order_quantity) == 0 or len(order_phone) == 0 or len(order_address) ==0 :
				context = {
					'error_message': "정보를 입력하세요!"
				}
				return render(request,'buy.html', context)

			
		except KeyError :
			context = {
				'error_message': "정보를 입력하세요!"
			}
			return render(request,'buy.html', context)
		else :
			menu = get_object_or_404(Menu, id=menu_id)
			order = menu.order_set.create(phone=order_phone,address=order_address,
					quantity=order_quantity,user_id=request.user.id)
			p = int(menu.price)
			q = int(order_quantity)
			result =  (p * q)
			context ={
				'menu' : menu,
				'order_address' : order_address,
				'order_phone' : order_phone,
				'order_quantity' : order_quantity,
				'order' : order,
				'result' : result
			}

			return render(request, 'pay_buy.html',context)

def mypage(request):
	if request.method == 'GET' :
		order_list = request.user.order_set.all()

		context = {
			'order_list' : order_list
		}

	return render(request, 'mypage.html', context)

def submit_pay(request):
	if request.method == 'POST' :
		menu_id = request.POST['menu_id']
		order_id = request.POST['order_id']

		try:
			menu = get_object_or_404(Menu, id=menu_id)
			order = get_object_or_404(Order, id=order_id)
			context = {
				'menu' : menu,
				'order' : order
			}
			return render(request, 'mypage.html', context)
			# return HttpResponseRedirect('/mypage/')

		except KeyError:
			return HttpResponse("Error!")



def submit_bucketlist(request):
	if request.method == 'POST' :

		menu_id = request.POST['menu_id']
		order_quantity = request.POST['order_quantity']

		try:
			menu = get_object_or_404(Menu, id=menu_id)
			bucketlist = menu.bucketlist_set.create(name=menu,user_id=request.user.id)
			
			return HttpResponseRedirect('/mypage/')

		except KeyError:

			return HttpResponse("Error!")

@login_required
def add_bucketlist(request, menu_id):

	menu = get_object_or_404(Menu, id=menu_id)

	context = {
		'menu_id' : menu_id,
		'menu' : menu
	}
	return render(request, 'add_bucketlist.html', context)


def signup(request):
	if request.method == 'GET' :
		return render(request, 'signup.html')
	elif request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		password_confirm = request.POST['password_confirm']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		if username.strip():
			if password == password_confirm:
				first_name.strip()
				last_name.strip()
				email.strip()
				user = User(username=username, password=password, first_name=first_name,last_name=last_name,email=email)
				user.set_password(password)
				user.save()
				return render(request, "signup_success.html")
			else : 
				return render(request, "signup.html",{
					"error_message" : 'Password 불일치!!!'
					})
		else :
			return render(request, "signup.html",{
					"error_message" : 'Username이 없습니다.입력하세요!!!'
				})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')






