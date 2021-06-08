from django.db import models
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint
from django.urls import reverse


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories',
                                     verbose_name='زیر مجمموعه', null=True, blank=True)
    is_sub = models.BooleanField(default=False, verbose_name='زیر مجموعه است')
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='شناسه')

    class Meta:
        ordering = ('name',)
        verbose_name = 'گروه'
        verbose_name_plural = '۱.گروه ها'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop:category_filter', args=[self.slug])


def random_int():
    return randint(10000000, 99999999)


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products', verbose_name='گروه')
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    slug = models.SlugField(verbose_name='شناسه', max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    inventory = models.SmallIntegerField(verbose_name='موجودی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد محصول')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروز رسانی محصول')
    code = models.IntegerField(default=random_int, editable=False, verbose_name='کد محصول')

    class Meta:
        ordering = ('name',)
        verbose_name = 'محصول'
        verbose_name_plural = '۲.محصولات'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop:product_detail',
    #                    args=[self.code, self.created.year, self.created.month, self.created.day, self.slug])


class ImageAlbum(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='album', verbose_name='محصول')

    def default(self):
        return self.images.filter(default=True).first()

    def thumbnails(self):
        return self.images.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return f"{self.product.name} - {self.product.category}"

    class Meta:
        verbose_name = 'آلبوم'
        verbose_name_plural = '۴.آلبوم ها'


class Picture(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='فایل عکس')
    default = models.BooleanField(default=False, verbose_name='پیش فرض')
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images', verbose_name='آلبوم عکس')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 800 or img.width > 800:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = '۳.عکس ها'

    def __str__(self):
        return f"{self.id} - {self.album.product.name} - {self.album.product.category}"


@receiver(post_save, sender=Product)
def save_image_album(sender, instance, created, **kwargs):
    if created:
        related_album = ImageAlbum(product=instance)
        related_album.save()
