from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.search import index

from ipac.models import Dreamer, Streamer, Seo


class Index(Page, Dreamer, Seo):
    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.Item']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        items = self.get_children().live().order_by('-first_published_at')
        context['items'] = items
        return context

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('end'),
    ]
    
    promote_panels = Page.promote_panels + Seo.panels


class Item(Page, Streamer, Seo):
    parent_page_types = ['tools.Index']
    # title = models.CharField(max_length=250)
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        # index.SearchField('title'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ] + Streamer.panels

    promote_panels = Page.promote_panels + Seo.panels
