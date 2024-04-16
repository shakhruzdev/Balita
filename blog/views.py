from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Contact, Comment, Category
import requests
from django.db.models import Count


def index_view(request):
    page = request.GET.get("page", 1)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:8]
    page_obj = Paginator(posts, 6)
    post_list = Post.objects.annotate(comment_count=Count('comments')).filter(
        comment_count__gt=0).order_by('-comment_count')
    d = {
        'posts': page_obj.page(page),
        'categories': categories,
        'post_list': post_list
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
    post_list = Post.objects.annotate(comment_count=Count('comments')).filter(
        comment_count__gt=0).order_by('-comment_count')

    return render(request, 'category.html',
                  context={'posts': page_obj.page(page), 'categories': categories, 'post_list': post_list})


def category_detail_view(request, pk):
    categories = Category.objects.all()
    if request.method == "POST":
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data.get("name"), email=data.get("email"),
                                     message=data.get("message"))
        obj.save()
        return redirect(f'/blog/{pk}')

    comments = Comment.objects.filter(post_id=pk)
    post = get_object_or_404(Post, pk=pk)
    related_posts = post.get_related_posts()
    return render(request, 'blog-single.html', context={'post': post, 'comments': comments, 'categories': categories, 'related_posts': related_posts})


def about_view(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:8]
    page = request.GET.get("page", 1)
    page_obj = Paginator(posts, 6)
    post_list = Post.objects.annotate(comment_count=Count('comments')).filter(
        comment_count__gt=0).order_by('-comment_count')
    return render(request, 'about.html',
                  context={'posts': page_obj.page(page), 'categories': categories, 'post_list': post_list})


def blog_search_view(request):
    text = request.GET.get('text', '')
    text = text.replace('+', ' ')
    if text:
        posts = Post.objects.filter(title__icontains=text)
    else:
        posts = Post.objects.all()
    return render(request, 'search_results.html', {'posts': posts, 'search_query': text})


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


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    related_posts = post.get_related_posts()
    return render(request, 'blog-single.html', {'post': post, 'related_posts': related_posts})
