from django.shortcuts import render,get_object_or_404,redirect
from blog_main.models import Category, Blog
from django.db.models import Q

# Create your views here.
def home(request):
    featured_post = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('updated_at')
    context = { 
        "featured_post": featured_post,
        "posts": posts,
    }
    return render(request, 'home.html', context)


def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status="Published", category=category_id)
    try:
        category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    context = {
        "posts": posts,
        "category": category,
    }
    return render(request, "posts_by_category.html", context)


def blogs(request, slug):
    single_post = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'single_post':single_post,
    }
    return render(request, "blogs.html", context)


def search(request):
    keyword = request.GET.get('keyword')
    
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)

