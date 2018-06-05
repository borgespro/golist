from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class List(BaseModel):
    owner = models.ForeignKey('users.User', related_name='lists', verbose_name=_('Owner'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100)
    valid_at = models.DateTimeField(_('Valid at'), null=True)

    def _is_active(self):
        return self.valid_at > timezone.now() if self.valid_at else True
    _is_active.boolean = True
    _is_active.short_description = _('Is it active?')
    is_active = property(_is_active)

    def _get_total_value(self):
        return self.list_items.annotate(total_price=F('quantity') * F('product__unit_price')).aggregate(
            total=Sum('total_price'))['total']
    total_value = property(_get_total_value)

    def _get_items_qty(self):
        return self.list_items.count()
    items_qty = property(_get_items_qty)

    def _get_products_qty(self):
        return self.list_items.aggregate(quantity=Sum('quantity'))['quantity']
    products_qty = property(_get_products_qty)

    class Meta:
        ordering = ['name', 'owner']

    def __str__(self):
        return self.name

    def add_item(self, product, quantity):
        return Item.objects.create(list=self, product=product, quantity=quantity)


class Item(BaseModel):
    list = models.ForeignKey('lists.List', verbose_name=_('List'), related_name='list_items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', verbose_name=_('Product'), on_delete=models.CASCADE, null=True)
    quantity = models.FloatField(_('Quantity'), default=0)

    def _get_total_price(self):
        if self.product:
            return self.product.unit_price * self.quantity
        return 0
    total_price = property(_get_total_price)

    class Meta:
        ordering = ['created_at', ]

    def __str__(self):
        return '{} ({})'.format(self.product.name, self.quantity)


