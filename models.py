from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet


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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # context['posts'] = self.posts
        context['item'] = self
        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()

        return context
    
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
        FieldPanel('intro', classname="full"),
    ] + Streamer.panels

    promote_panels = Page.promote_panels + Seo.panels

class ItemImage(Orderable):
    page = ParentalKey(Item, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class GoogleMaps(Page, Dreamer, Seo):
    template = 'home/google_maps.html'
    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.Item']

    # mapurl = models.URLField(null=True, blank=True)
    mapurl = models.CharField("Google Map URL", max_length=1500, null=True, blank=True)


    def get_context(self, request):
        context = super().get_context(request)
        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()

        return context

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('end'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('mapurl'),
        StreamFieldPanel('end'),
    ]
    
    promote_panels = Page.promote_panels + Seo.panels


class GoogleCalendar(Page, Dreamer, Seo):
    template = 'home/google_calendar.html'
    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.Item']

    calendarurl = models.URLField("URL for calendar", null=True, blank=True)


    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()

        return context

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('end'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('calendarurl'),
        StreamFieldPanel('end'),
    ]
    
    promote_panels = Page.promote_panels + Seo.panels



@register_snippet
class Social(models.Model):
    css = models.CharField("List CSS Classes (eg. text-primary py-0)", max_length=255, null=True, blank=True) # eg. text-primary py-0 fa-2x
    title = models.CharField("Title (eg. December Bulletin)", max_length=255, null=True, blank=True) # eg. Latest School Bulletin
    link = models.CharField("Link to resource (eg tel:+62-061-661-6765)", max_length=255, null=True, blank=True) # 
    icon = models.CharField("FA Icon (eg. fas fa-newspaper fa-fw fa-2x)", max_length=255, null=True, blank=True) 
    text = models.CharField("Description (eg. Latest School Bulletin)", max_length=255, null=True, blank=True) # eg. Decembers Bulletin

    panels = [
        FieldPanel('css'),
        FieldPanel('link'),
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.title