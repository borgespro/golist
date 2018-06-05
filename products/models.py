from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class Category(BaseModel):
    owner = models.ForeignKey('users.User', related_name='owner_categories', verbose_name=_('Owner'),
                              on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=30, db_index=True)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        ordering = ['title', ]


class Product(BaseModel):
    owner = models.ForeignKey('users.User', related_name='owner_products', verbose_name=_('Owner'),
                              on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', related_name='category_products', verbose_name=_('Category'),
                                 on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Title'), max_length=30, db_index=True)
    unit_price = models.FloatField(_('Unit Price'), default=0)

    class Meta:
        ordering = ['name', ]
