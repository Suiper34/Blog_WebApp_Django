import smtplib
from email.message import EmailMessage
from os import environ

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from users.decorators import admins_only
from dotenv import load_dotenv

from .forms import CreatePost, UsersComments
from .models import Comments, Post

load_dotenv()


def home(request):
    """Render the home page with latest blog posts."""
    blog_data = Post.objects.order_by('-date')[:3]
    return render(request, 'index.html', {
        'slice_blog_data': blog_data,
        'year': timezone.now().year,
        'current_user': request.user,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


def all_blogs(request):
    """Render paginated list of all blog posts."""
    page = request.GET.get('page', 1)
    blogs_per_page = Post.objects.all().order_by('-date')
    paginator = Paginator(blogs_per_page, 15)
    blogs = paginator.get_page(page)

    return render(request, 'allBlogs.html', {
        'blogs': blogs,
        'year': timezone.now().year,
        'current_user': request.user,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


def show_post(request, post_id):
    """Display a single blog post and handle comments."""
    post_to_disp = get_object_or_404(Post, id=post_id)
    comments_form = UsersComments()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Login to add comment!')
            return redirect('login')

        comments_form = UsersComments(request.POST)
        if comments_form.is_valid():
            user_comment = Comments(
                comment=comments_form.cleaned_data['comment'],
                the_user=request.user,
                post=post_to_disp
            )
            user_comment.save()

    comments = Comments.objects.filter(post_id=post_id)

    return render(request, 'post.html', {
        'post': post_to_disp,
        'year': timezone.now().year,
        'current_user': request.user,
        'form': comments_form,
        'comments': comments,
        'date_composed': post_to_disp.date.strftime('%Y-%m-%d'),
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


@login_required
def add_post(request):
    """
    Handle creation of new blog posts using the ModelForm (robust and safe).
    """
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            try:
                new_post = form.save(commit=False)
                new_post.author = request.user
                if not new_post.img_url:
                    new_post.img_url = '/static/assets/img/post-bg.jpg'
                new_post.save()
                messages.success(request, 'Successfully added!')
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'Post with this title already exists')
            except Exception as e:
                messages.error(request, 'Failed to add post')
                print(f'Error adding post: {str(e)}')

    else:
        form = CreatePost()

    return render(request, 'create_post.html', {
        'form': form,
        'year': timezone.now().year,
        'current_user': request.user,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


@login_required
@admins_only
def edit_post(request, post_id):
    """Handle editing of existing blog posts."""
    post_to_edit = get_object_or_404(Post, id=post_id)
    form = CreatePost(instance=post_to_edit)

    if request.method == 'POST':
        form = CreatePost(request.POST, instance=post_to_edit)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Post updated successfully!')
                return redirect('show_post', post_id=post_id)
            except IntegrityError:
                messages.error(
                    request, 'Your new title is used by someone...Modify it!')
            except Exception as e:
                messages.error(request, 'Failed to update!')
                print(f'Error: {str(e)}')

    return render(request, 'create_post.html', {
        'form': form,
        'year': timezone.now().year,
        'current_user': request.user,
        'is_existing': True,
        'post_title': post_to_edit.title,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


@login_required
@admins_only
def delete_post(request, post_id):
    """Delete a blog post."""
    post_to_delete = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post_to_delete.delete()
        messages.success(request, 'Post deleted!')
        return redirect('home')

    return render(request, 'confirm_delete.html', {
        'post': post_to_delete,
        'year': timezone.now().year,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
    })


def about_page(request):
    """Render the about page."""
    return render(request, 'about.html', {
        'year': timezone.now().year,
        'current_user': request.user,
        'year_of_exp': (timezone.now().year) - 2022,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
        'portfolio_site': environ.get('PORTFOLIO'),
    })


@login_required
def contact_page(request):
    """Handle contact form submissions."""
    if request.method == 'POST':
        username: str = request.POST.get('username')
        email: str = request.POST.get('email')
        subject: str = request.POST.get('subject')
        message: str = request.POST.get('message')

        with smtplib.SMTP_SSL('smtp.gmail.com') as mail_server:
            mail_server.login(
                user=environ.get('MAIL'),
                password=environ.get('PASSWORD')
            )
            mail = EmailMessage()
            mail['From'] = environ.get('MAIL')
            mail['To'] = email
            mail['Subject'] = f'{username}, {subject}'
            mail.set_content(message)
            mail_server.send_message(mail)

        return render(request, 'contact.html', {
            'year': timezone.now().year,
            'is_sent': True,
            'whatsapp': environ.get('WHATSAPP'),
            'github': environ.get('GITHUB'),
            'linkedin': environ.get('LINKEDIN'),
            'youtube': environ.get('YOUTUBE'),
            'tiktok': environ.get('TIKTOK'),
        })

    return render(request, 'contact.html', {
        'year': timezone.now().year,
        'current_user': request.user,
        'is_sent': False,
        'whatsapp': environ.get('WHATSAPP'),
        'github': environ.get('GITHUB'),
        'linkedin': environ.get('LINKEDIN'),
        'youtube': environ.get('YOUTUBE'),
        'tiktok': environ.get('TIKTOK'),
    })
