from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

import time

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.
class BlogIndexPage(Page):
	intro = RichTextField(blank=True)

	def get_content(self, request):
		context = super(BlogIndexPage, self).get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context

class BlogPageTag(TaggedItemBase):
	content_object = ParentalKey('BlogPage', related_name='tagged_items')

class BlogPage(Page):
	date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	body = RichTextField(blank=True)

	def main_image(self):
		gallery_item = self.gallery_images.first()
		if gallery_item:
			return gallery_item.image
		else:
			return None

	search_fields = Page.search_fields + [
	index.SearchField('intro'),
	index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
	MultiFieldPanel([
		FieldPanel('date'),
		# FieldPanel('tags'),
		], heading="Blog information"),
	FieldPanel('date'),
	FieldPanel('intro'),
	FieldPanel('body', classname="full"),
	InlinePanel('gallery_images', label="Gallery images"),
	]

class BlogPageGalleryImage(Orderable):
	page = ParentalKey(BlogPage, related_name='gallery_images')
	image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
	caption = models.CharField(blank=True, max_length=250)

	panels = [
	ImageChooserPanel('image'),
	FieldPanel('caption'),
	]
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