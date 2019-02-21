from django.shortcuts import get_object_or_404, redirect, render
from .models import Shop
from .forms import ShopForm


def index(request):
    # 전체 Shop 목록을 가져올 예정이다. (Lazy한 특성)
    qs = Shop.objects.all()
    return render(request, 'shop/shop_list.html', {
        'shop_list': qs,
    })


def shop_detail(request, pk):
    # 즉시 DB로부터 데이터를 가져옵니다.
    shop = Shop.objects.get(pk=pk)
    return render(request, 'shop/shop_detail.html', {
        'shop': shop,
    })


def shop_new(request):
    form_cls = ShopForm

    if request.method == "POST":  # "GET", "POST"
        form = form_cls(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save()
            return redirect(shop)
    else:
        form = form_cls()

    return render(request, 'shop/shop_form.html', {
        'form': form,
    })

from django.views.generic import CreateView

shop_new_cbv = CreateView.as_view(
    model=Shop, form_class=ShopForm)


def shop_edit(request, pk):
    # try:
    #     shop = Shop.objects.get(pk=pk)
    # except Shop.DoesNotExist:
    #     raise Http404  # django.http.Http404

    shop = get_object_or_404(Shop, pk=pk)

    form_cls = ShopForm

    if request.method == "POST":  # "GET", "POST"
        form = form_cls(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            shop = form.save()
            return redirect(shop)
    else:
        form = form_cls(instance=shop)

    return render(request, 'shop/shop_form.html', {
        'form': form,
    })


from django.views.generic import UpdateView

shop_edit_cbv = UpdateView.as_view(
    model=Shop, form_class=ShopForm)
