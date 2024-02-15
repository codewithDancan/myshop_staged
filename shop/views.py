from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'products': products})
 
def product_detail(request, slug, product_id):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    recently_viewed_products = []

    if 'recently_viewed' in request.session:
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)

        products = Product.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(products,
                                          key=lambda x: request.session['recently_viewed'].index(x.id))
        request.session['recently_viewed'].insert(0, product_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [product_id]

    request.session.modified = True

    context = {
        'product': product, 'cart_product_form': cart_product_form, 'recently_viewed_products': recently_viewed_products
     }
    return render(request, 'shop/product/detail.html', context)

# def product(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     recently_viewed_products = []
#     cart_product_form = CartAddProductForm()
#
#     # if 'recently_viewed' in request.session:
#     #     if product_id in request.session['recently_viewed']:
#     #         request.session['recently_viewed'].remove(product_id)
#     #
#     #     products = Product.objects.filter(pk__in=request.session['recently_viewed'])
#     #     recently_viewed_products = sorted(products,
#     #                                       key=lambda x: request.session['recently_viewed'].index(x.id))
#     #     request.session['recently_viewed'].insert(0, product_id)
#     #     if len(request.session['recently_viewed']) > 5:
#     #         request.session['recently_viewed'].pop()
#     # else:
#     #     request.session['recently_viewed'] = [product_id]
#     # print(recently_viewed_products)
#     # request.session.modified = True
#
#     context = {'product': product, 'recently_viewed_products': recently_viewed_products,
#                'cart_product_form': cart_product_form}
#     return render(request, 'shop/product/list.html', context)
    
     
