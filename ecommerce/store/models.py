from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
def category_products(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category__iexact=category)
    return render(request, 'partials/product_list.html', {'products': products})
    