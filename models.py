from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.search import index

from wagtail.admin.edit_handlers import FieldPanel
import datetime
today = datetime.date.today()

class Dreamer(models.Model):
    ''' Add DOUBLE streamer field to a page. '''
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)
    
    end = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)

    panels = [
        StreamFieldPanel('body'),
        StreamFieldPanel('end'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True

class Streamer(models.Model):
    ''' Add SINGLE streamer field to a page. '''
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)

    panels = [
        StreamFieldPanel('body'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True

class Seo(models.Model):
    ''' Add extra seo fields to pages such as icons. '''
    seo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        # default='media/images/default.png',
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional social media image 300x300px image < 300kb."
    )

    panels = [
        ImageChooserPanel('seo_image'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True


class Index(Page, Dreamer, Seo):
    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.Item']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        items = self.get_children().live().order_by('-first_published_at')
        context['items'] = items
        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()

        return context

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('end'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('end'),
    ]
    
    promote_panels = Page.promote_panels + Seo.panels


class Item(Page, Streamer, Seo):
    parent_page_types = ['tools.Index']
    intro = RichTextField(blank=True) # Shown on search index
    date = models.CharField(max_length=150, blank=True)
    auto_date = models.DateField(("Post date"), default=datetime.date.today)

    def get_context(self, request, *args, **kwargs):
        context = super(Index, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['item'] = self

        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()


        return context


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('auto_date'),
        FieldPanel('date'),
    ] + Streamer.panels

    promote_panels = Page.promote_panels + Seo.panels

class GoogleMaps(Page, Dreamer, Seo):
    template = 'home/google_maps.html'


class GoogleCalendar(Index):
    template = 'home/google_calendar.html'
