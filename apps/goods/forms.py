from django import forms

from goods.models import GoodsSkuInfo


class GoodsSkuInfoForm(forms.ModelForm):
   class Meta:
       model = GoodsSkuInfo