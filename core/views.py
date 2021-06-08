from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ImageAlbum
# from cart.forms import AddCartForm
from django.views.generic import View
from accounts.forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse


class Home(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'core/index.html', {'produsts': products})

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"{user.username} خوش آمدید")
                return redirect('core:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور صحیح نیست')
        return render(request, 'core/index.html')


def product_detail(request, code, year, month, day, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = product.category.all()
    main_category = categories.filter(is_sub=False)
    sub_categories = categories.filter(is_sub=True)
    # form = AddCartForm()
    return render(request, 'core/product.html',
                  {'product': product, 'main_category': main_category, 'sub_categories': sub_categories})
