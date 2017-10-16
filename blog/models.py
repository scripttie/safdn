from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index
import time

# Create your models here.
class BlogIndexPage(Page):
	intro = RichTextField(blank=True)

	def get_content(self, request):
		context = super(BlogIndexPage, self).get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context

	# date = models.DateField("Post date")
	# intro = models.CharField(max_length=250)
	# body = RichTextField(blank=True)

	# # new_field = models.CharField(max_length=140, default='SOME STRING')

	# search_fields = Page.search_fields + [
	# index.SearchField('intro'),
	# index.SearchField('body'),
	# ]

	# content_panels = Page.content_panels + [
	# FieldPanel('intro', classname="full")
	# ]