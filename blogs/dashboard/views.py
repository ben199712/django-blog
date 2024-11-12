from django.shortcuts import render, redirect, get_object_or_404
from blog_main.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogsForm, AddUserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()
    user_count = User.objects.all().count()

    context = {
        'category_count': category_count,
        'blog_count':blog_count,
        'user_count':user_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


def categories(request):
    return render(request, 'dashboard/categories.html')


def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("categories")
    form = CategoryForm()
    context = {

        'form':form,
    }
    return render(request, 'dashboard/add_categories.html', context)

def edit_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method =='POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request, 'dashboard/edit_categories.html', context)



def delete_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


#post views 
def posts(request):
    blogs = Blog.objects.all()
    context = {
        'blogs':blogs,
    }
    return render(request, "dashboard/posts.html", context)



def add_posts(request):
    if request.method == 'POST':
        form = BlogsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    form = BlogsForm()
    context = {
        'form':form, 
    }
    return render(request, 'dashboard/add_post.html', context)

def edit_posts(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            title = form.cleaned_data['title']
            blog.slug = slugify(title) + '-'+str(blog.id)
            blog.save()
            return redirect('posts')
    form = BlogsForm(instance=post)
    context = {
        'post':post,
        'form':form,
    }
    return render(request, 'dashboard/edit_post.html', context)


def delete_posts(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')



#users view
def user(request):
    user = User.objects.all()
    conttext = {
        'user':user
    }
    return render(request, 'dashboard/users.html', conttext)


def add_users(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')
        else:
            print(form.errors)
    form = AddUserForm()
    context = {
        'form':form,
    }
    return render(request, 'dashboard/add_users.html', context)


def edit_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user')
        else:
            print(form.errors)
    form = EditUserForm(instance=user)
    context = {
        'form':form,
    }
    return render(request, 'dashboard/edit_users.html', context)


def delete_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('user')
