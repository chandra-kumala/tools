from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.blocks import URLBlock, TextBlock, StructBlock, StreamBlock, CharBlock, RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class CommonStreamBlock(StreamBlock):
    heading = CharBlock(classname="full title", blank=True)
    paragraph = RichTextBlock(blank=True)
    embed = EmbedBlock(blank=True)
    image = ImageChooserBlock(blank=True)
    buttonLink = StructBlock([
        ('text', TextBlock(blank=True)),
        ('link', URLBlock(label="external URL", blank=True)),
    ])

    class Meta:
        icon = 'cogs'


class Dreamer(models.Model):
    ''' Add DOUBLE streamer field to a page. '''
    body = StreamField(CommonStreamBlock(), null=True, blank=True,)
    end = StreamField(CommonStreamBlock(), null=True, blank=True,)

    panels = [
        StreamFieldPanel('body'),
        StreamFieldPanel('end'),
    ]

    class Meta:
        """Abstract Model."""
        
        abstract = True 


class Seo(models.Model):
    ''' Add extra seo fields to pages such as icons. '''
    google_ad_code = models.CharField(max_length=50, null=True, blank=True)
    seo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional social media image 300x300px image < 300kb."
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('seo_image'),
                FieldPanel('google_ad_code'),
            ],
            heading="Additional SEO options ...",
        )

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
        context['menuitems'] = request.site.root_page.get_descendants(
            inclusive=True).live().in_menu()

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


class Item(Page, Seo):
    parent_page_types = ['tools.Index']
    text = RichTextField(blank=True)  # Shown on search index

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['item'] = self
        items = self.get_siblings(
            inclusive=False).live().order_by('-first_published_at')
        context['items'] = items
        context['menuitems'] = request.site.root_page.get_descendants(
            inclusive=True).live().in_menu()

        return context

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('text'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('text', classname="full"),
        InlinePanel('gallery_images', label="Index page images"),
    ]

    promote_panels = Page.promote_panels + Seo.panels


class ItemImage(Orderable):
    page = ParentalKey(Item, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]



@register_snippet
class Social(models.Model):
    css = models.CharField("List CSS Classes (eg. text-primary py-0)",
                           max_length=255, null=True, blank=True)  # eg. text-primary py-0 fa-2x
    title = models.CharField("Title (eg. December Bulletin)", max_length=255,
                             null=True, blank=True)  # eg. Latest School Bulletin
    link = models.CharField(
        "Link to resource (eg tel:+62-061-661-6765)", max_length=255, null=True, blank=True)
    icon = models.CharField(
        "FA Icon (eg. fas fa-newspaper fa-fw fa-2x)", max_length=255, null=True, blank=True)
    text = models.CharField("Description (eg. Latest School Bulletin)",
                            max_length=255, null=True, blank=True)  # eg. Decembers Bulletin

    panels = [
        FieldPanel('css'),
        FieldPanel('link'),
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.title
