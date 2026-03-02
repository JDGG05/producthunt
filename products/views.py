from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})

@login_required

def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            product.url = request.POST['url']
            if product.url.startswith('http://') or product.url.startswith('https://'):
                product.url = product.url
            else:
                product.url = 'http://' + product.url
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            
            product.pub_date = timezone.now()
            
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/create.html')
    
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # product is already fetched; pass it directly to template
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))