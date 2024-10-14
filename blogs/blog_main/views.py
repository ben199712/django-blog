from django.shortcuts import render,get_object_or_404,redirect
from blog_main.models import Category, Blog

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