from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from newboard.models import Board, Article, Reply
from django.contrib.auth.models import User

#---------- Landing page start -----------#
def index(request):
	boards = Board.objects.order_by("title")
	dashboards = []
	for board in boards:
		articles = board.article_set.order_by("-written_date")[:5]
		list_item = {
			"board" : board,
			"latest_articles" : articles
		}
		dashboards = dashboards + [list_item]

	context = {
	"boards" : boards,
	"dashboards" : dashboards
	}
	return render(request, "index.html", context)
#---------- Landing page end -----------#

#---------- board start -----------#
@login_required
def board(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	article_list = board.article_set.order_by("-written_date")
	paginator = Paginator(article_list, 5)
	page = request.GET.get("page")
	error_message = None
	try:
		if request.session['error'] != None :
			error_message = request.session["error"]
			del request.session["error"]
	except KeyError:
		pass	


	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)

	return render(request, "board.html", { 
		"board": board, 
		"articles": articles ,
		"pages": paginator.page_range,
		"error_message" : error_message
	})

@login_required
def board_search(request, board_id) :
	board = get_object_or_404(Board, id=board_id)
	keyword = ""
	if request.method =="POST" :
		try:
			keyword = request.POST["search_keyword"].strip()
		except KeyError :
			pass
	else :
		try :
			keyword = request.GET["search_keyword"].strip()
		except KeyError :
			pass

	if len(keyword) == 0 :
		request.session["error"] = "검색어를 입력하세요"
		return HttpResponseRedirect("/board/%s/" %(board_id,))
	article_list = board.article_set.filter(title__contains=keyword).order_by("-written_date")
	paginator = Paginator(article_list,5)
	page = request.GET.get('page')

	try :
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)

	return render(request, "search.html", { 
		"board": board, 
		"articles": articles,
		"keyword" : keyword,
		"pages": paginator.page_range
	})

# @login_required
# def new_board(request):
# 	return render(request, "create_board.html", {})

@login_required
def submit_board(request):
	boards = Board.objects.order_by("title")
	dashboards = []
	for board in boards :
		articles = board.article_set.order_by("-written_date")[:5]
		list_item = {
			"board" : board,
			"latest_articles" : articles
		}
		dashboards = dashboards + [list_item]
	try:
		board_title = request.POST["board_title"]
	except KeyError:
		context = { 
			"boards" : boards,
			"dashboards" : dashboards,
			"error_message": "입력이 올바르지 않습니다."
		}
		return render(request, "index.html", context)

	else:
		if len(board_title.strip()) == 0 :
			context = { 
				"boards" : boards,
				"dashboards" : dashboards,
				"error_message": "입력이 올바르지 않습니다."
			}
			return render(request, "index.html", context)

		if request.user.is_superuser == False :
			context = {
				"error_message" : "권한이 없습니다."
			}
			return render(request, "index.html", context)
			
		board = Board(title=board_title)
		board.save()
		return HttpResponseRedirect("/")
#---------- board end -----------#

#---------- article start -----------#
@login_required
def article(request, board_id, article_id):
	article = get_object_or_404(Article, id=article_id)
	reply_list = article.reply_set.order_by("written_date")
	
	context = {
		"article" : article,
		"replies" : reply_list
	}
	return render(request, "article.html", context)

@login_required
def new_article(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	context = { "board_id": board_id,
				"board" : board
	}
	return render(request, "write_article.html", context)

@login_required
def submit_article(request, board_id):
	try:
		article_title = request.POST["article_title"]
		article_content = request.POST["article_content"]
	except KeyError:
		context = { 
			"error_message": "올바르지 않은 입력입니다",
			"board_id" : board_id
		}
		return render(request, "write_article.html", context)
	else:
		if len(article_title.strip()) == 0 or len(article_content.strip()) == 0 :
			context = {
				"error_message" : "제목 또는 내용은 반드시 존재해야 합니다.",
				"board_id" : board_id
			}
			return render(request, "write_article.html", context)

		board = get_object_or_404(Board, id=board_id)

		board.article_set.create(title=article_title, content=article_content, user_id=request.user.id)
		return HttpResponseRedirect("/board/%s" % (board_id,))

@login_required
def delete_article(request, board_id, article_id) : 
	article = get_object_or_404(Article, id=article_id)
	if article.user.id != request.user.id :
		article = get_object_or_404(Article, id=article_id)
		reply_list = article.reply_set.order_by("written_date")
		context = {
			"error_message" : "작성자가 아닙니다"
		}
		return render(request, "article.html", context)
	else:
		article.delete()
		return HttpResponseRedirect("/board/%s" % (board_id,))

#---------- article end -----------#

#---------- reply start -----------#
@login_required
def new_reply(request, board_id, article_id):
	article = get_object_or_404(Article, id=article_id)
	reply_list = article.reply_set.order_by("written_date")

	try:
		reply_content = request.POST["reply_content"]
	except KeyError:
		context = { 
			"article": article, 
			"error_message": "올바르지 않은 입력입니다",
			"replies" : reply_list
		}
		return render(request, "article.html", context)
	else:
		if len(reply_content.strip()) == 0 :
			context = { 
				"article": article, 
				"error_message": "댓글의 내용이 반드시 존재해야 합니다",
				"replies" : reply_list
			}
			return render(request, "article.html", context)	
		article.reply_set.create(content=reply_content, user_id=request.user.id)
		return HttpResponseRedirect("/board/%s/%s" % (board_id, article_id,))

@login_required
def delete_reply(request, board_id, article_id, reply_id):
	reply = get_object_or_404(Reply, id=reply_id)
	if reply.user.id != request.user.id :
		article = get_object_or_404(Article, id=article_id)
		reply_list = article.reply_set.order_by("written_date")
		context = {
			"error_message" : "작성자가 아닙니다.",
			"replies" : reply_list,
			"article" : article
		}
		return render(request, "article.html", context)
	else :
		reply.delete()
		return HttpResponseRedirect("/board/%s/%s" % (board_id, article_id,))
#---------- reply end -----------#

#---------- authentication start -----------#

def signup(request) :
	error_message = None
	try :
		if request.session["error"] != None :
			error_message = request.session["error"]
			del request.session["error"]
	except KeyError :
		pass

	return render(request, "signup.html",{
			"error_message" : error_message
		})


def signup_submit(request) :
	try :
		username = request.POST["username"].strip()
		password = request.POST["password"].strip()
		password_confirm = request.POST["password_confirm"].strip()
		first_name = request.POST["first_name"].strip()
		last_name = request.POST["last_name"].strip()

		if len(username) == 0 or len(password) == 0 or len(password_confirm) == 0 or len(first_name) == 0 or len(last_name) == 0:
			request.session["error"] = "입력값이 올바르지 않습니다"
			return HttpResponseRedirect("/signup/")

	except KeyError :
		request.session["error"] = "올바르지 않은 요청입니다."
		return HttpResponseRedirect("/signup/")

	user = User(username = username, first_name = first_name, last_name = last_name)
	user.set_password(password)

	user.save()
	return HttpResponseRedirect("/")

def user_logout(request) :
	logout(request)
	return HttpResponseRedirect("/")

#---------- authentication end -----------#