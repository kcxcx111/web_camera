from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Featured products for homepage
    featured_products = Product.objects.filter(featured=True, available=True)[:4]
    
    query = request.GET.get('q')
    if query:
        # Split the query into words for more accurate matching
        query_words = query.split()
        
        # Start with a base query
        query_filter = Q()
        
        # Add conditions for each word
        for word in query_words:
            query_filter |= Q(name__icontains=word)
            query_filter |= Q(description__icontains=word)
            query_filter |= Q(category__name__icontains=word)
            # Include specifications in search
            query_filter |= Q(specifications__name__icontains=word)
            query_filter |= Q(specifications__value__icontains=word)
        
        # Apply the filter and get distinct products
        products = products.filter(query_filter).distinct()
        
        # Sort by relevance (more matches = higher relevance)
        products = sorted(products, key=lambda p: sum(
            # Count matches in product name (higher weight)
            (word.lower() in p.name.lower()) * 3 +
            # Count matches in description
            (word.lower() in p.description.lower()) +
            # Count matches in category
            (word.lower() in p.category.name.lower()) +
            # Count matches in specifications
            sum((word.lower() in spec.name.lower() or word.lower() in spec.value.lower()) 
                for spec in p.specifications.all()) * 2
            for word in query_words
        ), reverse=True)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'featured_products': featured_products
    }
    
    return render(request, 'store/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'store/product_detail.html', context)

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if query and len(query.strip()) > 0:  # Accept any length of query, including single characters
        # Split the query into words for more accurate matching
        query_words = query.split()
        
        # Start with a base query
        query_filter = Q()
        
        # Add conditions for each word
        for word in query_words:
            query_filter |= Q(name__icontains=word)
            query_filter |= Q(description__icontains=word)
            query_filter |= Q(category__name__icontains=word)
            # Include specifications in search
            query_filter |= Q(specifications__name__icontains=word)
            query_filter |= Q(specifications__value__icontains=word)
        
        # Apply the filter and get distinct products
        products = products.filter(query_filter).distinct()
        
        # Sort by relevance (more matches = higher relevance)
        products = sorted(products, key=lambda p: sum(
            # Count matches in product name (higher weight)
            (word.lower() in p.name.lower()) * 3 +
            # Count matches in description
            (word.lower() in p.description.lower()) +
            # Count matches in category
            (word.lower() in p.category.name.lower()) +
            # Count matches in specifications
            sum((word.lower() in spec.name.lower() or word.lower() in spec.value.lower()) 
                for spec in p.specifications.all()) * 2
            for word in query_words
        ), reverse=True)
    
    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query
    })

def search_products_api(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    results = []
    
    if query and len(query.strip()) > 0:  # Accept any length of query, including single characters
        # Split the query into words for more accurate matching
        query_words = query.split()
        
        # Start with a base query
        query_filter = Q()
        
        # Add conditions for each word
        for word in query_words:
            query_filter |= Q(name__icontains=word)
            query_filter |= Q(description__icontains=word)
            query_filter |= Q(category__name__icontains=word)
            # Include specifications in search
            query_filter |= Q(specifications__name__icontains=word)
            query_filter |= Q(specifications__value__icontains=word)
        
        # Apply the filter and get distinct products
        products = products.filter(query_filter).distinct()
        
        # Sort by relevance (more matches = higher relevance)
        # This is a simple approach - for more complex relevance scoring,
        # you might need a dedicated search engine like Elasticsearch
        products = sorted(products, key=lambda p: sum(
            # Count matches in product name (higher weight)
            (word.lower() in p.name.lower()) * 3 +
            # Count matches in description
            (word.lower() in p.description.lower()) +
            # Count matches in category
            (word.lower() in p.category.name.lower()) +
            # Count matches in specifications
            sum((word.lower() in spec.name.lower() or word.lower() in spec.value.lower()) 
                for spec in p.specifications.all()) * 2
            for word in query_words
        ), reverse=True)
        
        # Limit to top 20 results for showing more options
        products = products[:20]
        
        # Format the results
        for product in products:
            # Get key specifications (if any)
            specs = []
            for spec in product.specifications.all()[:2]:  # Limit to 2 key specs
                specs.append(f"{spec.name}: {spec.value}")
            
            results.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'category': product.category.name,
                'image': product.image.url if product.image else None,
                'url': product.get_absolute_url(),
                'specs': specs,
            })
    
    return JsonResponse({'results': results})
