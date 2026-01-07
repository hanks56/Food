from django.shortcuts import render
from applications.category.restaurants.models import Restaurant
from applications.category.market.models import MarketProduct

def index_view(request):
    restaurants = Restaurant.objects.order_by('-rating')[:4]
    market_products = MarketProduct.objects.all()[:4]
    
    context = {
        'restaurants': restaurants,
        'market_products': market_products,
    }
    return render(request, 'index.html', context)