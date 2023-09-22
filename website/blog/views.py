from django.shortcuts import render, get_object_or_404

from blog.models import Post


def blogView(request):
    """Вьюха страницы блога"""
    title = 'Статьи Натэкс'
    description = 'Статьи Оценочная экспертная компания'
    template = 'blog.html'
    posts = Post.objects.all()
    context = {'title': title,
               'description': description,
               'posts': posts}
    return render(request, template, context)


def postView(request, post_slug):
    """Вьюха страницы блога"""
    post = get_object_or_404(Post, slug=post_slug)
    template = 'post.html'
    context = {'title': post.title,
               'description': post.description,
               'post': post}
    return render(request, template, context)
