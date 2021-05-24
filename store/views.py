from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from .models import Product


def create_shopping_basket(request):
    # создать корзину если еще нету
    s_basket_list = request.session.get('s_basket')
    if not s_basket_list:
        s_basket_list = []
    return s_basket_list

def basket_value_and_sum(request):
    b_sum = 0
    products = Product.objects.filter(in_stock=True)
    s_basket_list = create_shopping_basket(request)
    
    products_ids = [i.id for i in products]
    for product_id in s_basket_list:
        # синхронизировать корзину с товарами в наличии
        if product_id not in products_ids:
           s_basket_list.remove(product_id) 
        else:
            try:
                # сложить сумму товаров в корзине
                b_sum += Product.objects.get(id=product_id).price
            except Product.DoesNotExist:
                pass

    request.session['s_basket'] = s_basket_list

    return b_sum


def index(request):
    # in_stock=True в наличии
    products_for_sale =reversed(Product.objects.filter(in_stock=True))
    s_basket_sum = basket_value_and_sum(request)

    context = {
    'products_for_sale': products_for_sale,
    's_basket_sum': s_basket_sum,
    }
    return render(request, 'store/index.html', context)


def detail(request, product_id):
    current_product = get_object_or_404(Product, pk=product_id)
    s_basket_sum = basket_value_and_sum(request)

    context = {
        'current_product': current_product,
        's_basket_sum': s_basket_sum,
    }
    return render(request, 'store/detail.html', context)

def basket(request):
    # корзина товаров
    s_basket_list = request.session.get('s_basket')
    products_in_basket = Product.objects.filter(in_stock=True, pk__in=s_basket_list)
    s_basket_sum = basket_value_and_sum(request)

    context = {
        'products_in_basket': products_in_basket,
        's_basket_sum': s_basket_sum,
    }
    return render(request, 'store/basket.html', context)


@require_http_methods(["POST"])
def add_product_to_s_basket(request, product_id):
    # add product to shopping basket

    # существует ли продукт, если нет 404
    get_object_or_404(Product, pk=product_id)

    s_basket_list = create_shopping_basket(request)
        
    if product_id in s_basket_list:
        return HttpResponse('404, already added')
    
    s_basket_list.append(product_id)
    request.session['s_basket'] = s_basket_list
    
    next = request.META.get('HTTP_REFERER')
    messages.error(request, '+ корзина')
    return HttpResponseRedirect(next)


@require_http_methods(["POST"])
def delete_product_from_s_basket(request, product_id):
    # delete one from shopping basket

    # существует ли продукт, если нет 404
    get_object_or_404(Product, pk=product_id)
    
    s_basket_list = request.session.get('s_basket')
    
    s_basket_list.remove(product_id)
    request.session['s_basket'] = s_basket_list
    
    return HttpResponseRedirect(reverse('store:basket'))
        

@require_http_methods(["POST"])       
def clear_s_basket(request):
    try:
        del request.session['s_basket']
    except KeyError:
        pass

    return HttpResponseRedirect(reverse('store:index'))