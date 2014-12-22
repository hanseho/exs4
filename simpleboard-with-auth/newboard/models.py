from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
	title = models.CharField('title', max_length=200)
	created_date = models.DateTimeField('written date', auto_now_add=True)
	
	def __str__(self):
		return self.title

class Article(models.Model):
	board = models.ForeignKey(Board)
	user = models.ForeignKey(User)
	title = models.CharField('title', max_length=200)
	content = models.TextField('contents', default="")
	written_date = models.DateTimeField('written date', auto_now_add=True)
	update_date = models.DateTimeField('update date', auto_now=True)

	def __str__(self):
		return "%s : %s" % (self.title, self.content)

class Reply(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(User)
	content = models.TextField('reply')
	written_date = models.DateTimeField('written_date', auto_now_add=True)

	def __str__(self):
		return "Re: %s, %s" % (self.article.title, self.content)
