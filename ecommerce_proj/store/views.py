from django.shortcuts import render
from . models import Category, Product

def shop(request,category_id = None):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get('category',None)
    if category_id:
        products = products.filter(product_category_id = category_id)

    context = {
        'categories' : categories,
        'products' : products
    }

    return render(request,'shop.html',context)


def single(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.exclude(id=product_id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'product-single.html', context)