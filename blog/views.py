from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.timezone import now

from .models import Post, Tag, Category, Subscribe, Comment, Profile_WER, PostsPhoto
from .forms import PostForm, SubscribeForm, PostsPhotoFormSet, ChangeUserForm, ProfileWERForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    return {"cats1": all[:half], "cats2": all[half:]}


def get_tags():
    all_tags = Tag.objects.all()
    return {"all_tags": all_tags}


def index(request):
    posts = Post.objects.all().order_by("-published_data")
    imgs = PostsPhoto.objects.all()
    paginator = Paginator(posts,2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # posts = Post.objects.filter(title__contains="python")
    # posts = Post.objects.filter(published_data__year=2023)
    # posts = Post.objects.filter(content__startswith="Lorem")
    # posts = Post.objects.filter(category__name__iexact="it")
    tags = get_tags().values()
    context = {'posts': posts, "tags": tags, "imgs": imgs}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context)


def post(request, title=None):
    post = get_object_or_404(Post, title=title)
    comments = Comment.objects.filter(post=post)
    tags_for_post = Tag.objects.filter(posts=post)
    imgs = PostsPhoto.objects.filter(post=post)
    context = {"post": post, "comments": comments, "tags_for_post": tags_for_post, "imgs": imgs}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/post.html", context)


def about(request):
    context = {}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/about.html", context)


def contact(request):
    context = {}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/contact.html", context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by("-published_data")
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context)


def tag(request, name=None):
    tag = get_object_or_404(Tag, name=name)
    posts = tag.posts.all()
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context)


def search(request):
    query = request.GET.get("query")
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = PostsPhotoFormSet(request.POST, request.FILES,
                                    queryset=PostsPhoto.objects.none())  # Пустой queryset для отображения пустых форм
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.published_data = now()
            post.user = request.user
            post.save()
            formset.instance = post
            formset.save()
            return redirect('index')
    else:
        form = PostForm()
        formset = PostsPhotoFormSet(queryset=PostsPhoto.objects.none())  # Пустой queryset для отображения пустых форм
    context = {'form': form, 'formset': formset}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/create.html", context)


def subscribe(request):
    if request.method == 'POST':
        form_sub = SubscribeForm(request.POST)
        if form_sub.is_valid():
            sub = form_sub.save(commit=False)
            sub.save()
            return redirect("index")
    form_sub = SubscribeForm()
    context = {'form_sub': form_sub}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, "blog/index.html", context)


def add_comment(request, title=None):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        post = get_object_or_404(Post, title=title)
        comment = Comment(author=request.user, text=comment_text, post=post)
        comment.date = now()
        comment.save()
        return redirect('post', title=title)
    else:
        return redirect('index')


class MyLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


def user_profile(request, id):
    profile = get_object_or_404(User, id=id)
    count_post = Post.objects.filter(user=id).count()
    context = {"profile": profile, "count_post": count_post}
    context.update(get_tags())
    context.update(get_categories())
    return render(request, "blog/user_profile.html", context)


def set_ava(request, id):
    profile = get_object_or_404(Profile_WER, id=id)
    user = User.objects.get(id=profile.id)
    if request.method == "POST":
        set_ava_form = ProfileWERForm(request.POST, request.FILES)
        if set_ava_form.is_valid():
            profile.avatar = request.FILES['avatar']
            profile.user = user
            profile.save()
            return redirect('index')
    else:
        set_ava_form = ProfileWERForm()
    return render(request, "blog/user_profile.html", {"set_ava_form": set_ava_form})


def update_profile(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        change_info = ChangeUserForm(request.POST, instance=user)
        if change_info.is_valid():
            change_info.save()
            return redirect("index")
    change_form = ChangeUserForm()
    context = {"change_form": change_form}
    return render(request, "blog/update_profile.html", context)


def reg_user(request):
    if request.method == "POST":
        user_new = UserCreationForm(request.POST)
        if user_new.is_valid():
            user = user_new.save()
            username = user_new.cleaned_data.get("username")
            password = user_new.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("index")
    new_user = UserCreationForm()
    context = {"new_user": new_user}
    return render(request, "blog/reg_user.html", context)


"rwtetdfsdf23"
