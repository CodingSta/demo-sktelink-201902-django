from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'  # 모든 필드 가져오기
        # fields = ['title', 'content']  # 지정 필드만 가져오기
