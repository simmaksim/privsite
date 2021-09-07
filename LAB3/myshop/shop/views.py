from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
import logging
from .models import *
from .serializers import ProductSerializer
from rest_framework import generics


info_logger = logging.getLogger('My shop')
info_logger.setLevel(logging.INFO)
filehandler = logging.FileHandler('MyShop.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
info_logger.addHandler(filehandler)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Customer.objects.create(
                user=user
            )
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            info_logger.info('Created new customer')
            return redirect('/login')
        else:
            info_logger.warning('Invalid registration')

    context = {'form': form}
    return render(request, 'shop/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            info_logger.info('Log in succesed')
            return redirect('/')
        else:
            info_logger.warning('Wrong input')
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'shop/login.html', context)


def logoutPage(request):
    logout(request)
    info_logger.info('User logouted')
    return redirect('/login')

@login_required(login_url='/login')
def product_list(request, category_slug=None, tag_slug=None):
    category = None
    categories = Category.objects.all()
    tag = None
    tags = Tag.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    #if tag_slug:
     #   tag = get_object_or_404(Tag, slug=tag_slug)
      #  products = products.filter(tag=tag)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                  # 'tag': tag,
                  # 'tags': tags,
                   'products': products})

@login_required(login_url='/login')
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


class APIProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class APIProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



