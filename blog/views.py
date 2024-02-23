from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Contact, Comment, Category
import requests


def index_view(request):
    page = request.GET.get("page", 1)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:8]
    page_obj = Paginator(posts, 6)
    d = {
        'posts': page_obj.page(page),
        'categories': categories
    }

    return render(request, 'index.html', context=d)


def category_view(request):
    data = request.GET
    cat = data.get("cat")
    page = data.get("page", 1)
    categories = Category.objects.all()
    if cat:

        posts = Post.objects.filter(is_published=True, category__id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')

    page_obj = Paginator(posts, 6)
    return render(request, 'category.html', context={'posts': page_obj.page(page), 'categories': categories})


def category_detail_view(request, pk):
    categories = Category.objects.all()
    if request.method == "POST":
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data.get("name"), email=data.get("email"),
                                     message=data.get("message"))
        obj.save()
        return redirect(f'/blog/{pk}')

    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk)
    return render(request, 'blog-single.html', context={'post': post, 'comments': comments, 'categories': categories})


def about_view(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:8]
    page = request.GET.get("page", 1)
    page_obj = Paginator(posts, 6)
    return render(request, 'about.html', context={'posts': page_obj.page(page), 'categories': categories})


def contact_view(request):
    print("=" * 50)
    print(request.method)
    print("=" * 50)
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST

        obj = Contact.objects.create(name=data.get("name"), email=data.get("email"),
                                     message=data.get("message"), phone=data.get("phone"))
        obj.save()

        token = '7160148764:AAGATAAOooZunLW8gMTi_EZ1Vp2GxuRuLMs'
        requests.get(
            f"""https://api.telegram.org/bot{token}/sendMessage?chat_id=5467422443&text=BALITA\nname: {obj.name}\nphone: {obj.phone}\nemail: {obj.email}\nmessage: {obj.message}""")

        return redirect('/contact')
    return render(request, 'contact.html', context={'categories': categories})
