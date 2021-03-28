from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from frontend.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.forms import CommentForm
from backend.forms import ReviewForm
from backend.forms import FilterForm
from django.db.models import Count, Q
from .filters import HotelFilter



# Create your views here.

def index(request):
    news = Blog.objects.order_by('-date')[:4]
    latest = Hotel.objects.order_by('-date')[:4]
    featured = Hotel.objects.order_by('-date').filter(featured=True)[:4]
    sponsored = Hotel.objects.order_by('-date').filter(sponsored=True)[:4]
    agents = UserProfile.objects.all()
    location = Location.objects.all()
    query_form = FilterForm(request.GET)

    context = {
        'latest': latest,
        'news': news,
        'featured': featured,
        'sponsored': sponsored, 
        'agents': agents, 
        'location': location,
        'queryf': query_form
    }

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save() 

    return render(request, 'frontend/index.html', context)

def homepage(request):
    news = Blog.objects.order_by('-date')[:4]
    latest = Hotel.objects.order_by('-date')[:4]
    featured = Hotel.objects.order_by('-date').filter(featured=True)[:4]
    sponsored = Hotel.objects.order_by('-date').filter(sponsored=True)[:4]
    agents = UserProfile.objects.all()

    context = {
        'latest': latest,
        'news': news,
        'featured': featured,
        'sponsored': sponsored, 
        'agents': agents
    }

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save() 

    return render(request, 'frontend/homepage2.html', context)

def about(request):
    about = About.objects.all()
    user_var = User.objects.order_by('-last_name')
    context = {'abt':about, 'user':user_var}
    return render(request, 'frontend/about.html', context)

def about_detail(request, abt_id):
    detail = About.objects.get(id=abt_id)
    return render(request, 'frontend/about_detail.html', {'det':detail})

def blog(request):
    most_recent = Blog.objects.order_by('-date')[:4]
    agents = UserProfile.objects.all()
    blg_post = Blog.objects.order_by('-date')
    paginated_filter = Paginator(blg_post, 3)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filter.get_page(page_number)
    context = {
        'person_page_obj': blg_post, 
        'most_recent': most_recent,
        'agents': agents
    }
    context['person_page_obj'] = person_page_obj

    return render(request, 'frontend/blog.html', context)

def hotel(request):
    most_recent = Hotel.objects.order_by('-date')[:4]
    query_form = FilterForm(request.GET)
    all_post = Hotel.objects.order_by('-date')
    paginated_filter = Paginator(all_post, 4)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filter.get_page(page_number)
    context = {
        'person_page_obj': all_post, 
        'most_recent': most_recent,
        'queryf': query_form
    }
    context['person_page_obj'] = person_page_obj

    return render(request, 'frontend/hotels-grid-sidebar-2.html', context)


def hotel_detail(request, pk):
    post = get_object_or_404(Hotel, pk=pk)
    reviews = Review.objects.filter(post=pk).order_by('-timestamp')
    if request.method == "POST":
        Rform = ReviewForm(request.POST)
        if Rform.is_valid():
            review = Rform.save(commit=False) 
            review.post = post
            review.save()
            return redirect('frontend:hotel_detail', pk=post.pk)
    else:
        Rform = ReviewForm()
    return render(request, 'frontend/hotel-detail.html', {'pst':post, 'Rform':Rform, 'revs':reviews})


def blog_post(request, pk):
    # single_post = Blog.objects.get(pk=pk)
    single_post = get_object_or_404(Blog, pk=pk)
    comments = Comment.objects.filter(post=pk).order_by('-timestamp')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.post = single_post
            comment.save()
            return redirect('frontend:blog_post', pk=single_post.pk)
        #  single_post = {'form': form, 'most_recent': most_recent,}
    else:
        form = CommentForm()
    return render(request, 'frontend/blog-post.html', {'comm':comments, 'form':form, 'sipst':single_post})

def help(request):
    return render(request, 'frontend/help.html')

def faq(request):
    return render(request, 'frontend/faq.html')

def contact(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = 'Contact Us Information'
        context = {
            'name':name,
            'lastname':lastname,
            'phone':phone,
            'email':email,
            'message': message
        }
        html_message = render_to_string('frontend/mail-template.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From GAlAXY <tijaniyunus07@gmail.com>'
        send = mail.send_mail(subject, plain_message, from_email, [
                    'teezee132@gmail.com', 'tijaniyunus07@gmail.com', email], html_message=html_message, fail_silently=True)
        if send:
            messages.success(request, 'Email sent')
        else:
            messages.error(request, 'Mail not sent')

    return render(request, 'frontend/contacts.html')

def post_from_cat(request, category_id):
    count_post = Hotel.objects.filter(cat_id__id=category_id).count()
    try:
        get_cat_name = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return render(request, 'frontend/404.html')
    # get_cat_name = Category.objects.get(id=category_id)
    post_cat= Hotel.objects.filter(cat_id__id=category_id)
    context = {'posts': post_cat, 'counts': count_post, 'cat': get_cat_name}
    return render(request, 'frontend/post-cat.html', context)



def post_from_location(request, location_id):
    query_form = FilterForm(request.GET)
    count_post = Hotel.objects.filter(location_id__id=location_id).count()
    try:
        get_location_name = Location.objects.get(id=location_id)
        
    except ObjectDoesNotExist:
        return render(request, 'frontend/404.html')
    # get_cat_name = Category.objects.get(id=category_id)
    # paginated_filter = Paginator(get_location_name, 3)
    # page_number = request.GET.get('page')
    # person_page_obj = paginated_filter.get_page(page_number)
    post_location= Hotel.objects.filter(location_id__id=location_id)
    
        
    context = {'posts': post_location, 'counts': count_post, 'loc': get_location_name, 'queryf': query_form}
    # context['person_page_obj'] = person_page_obj

    return render(request, 'frontend/post-location.html', context)

def search(request):
    queryset = Blog.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(blg_title__icontains=query) |
            Q(blg_content__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
        
    }
    return render(request, 'frontend/search_results.html', context)


def filter_search(request):
    queryset = Hotel.objects.all()
    query = request.GET.get('f')
    if query:
        queryset = queryset.filter(
            Q(price__icontains=query) 
        ).distinct()
    else:
         queryset = Hotel.objects.all()
    context = {
         'queryset': queryset
    }
    return render(request, 'frontend/filtersearch.html', context)


def filtersearch(request):
    if request.method == 'GET':
        query_form = FilterForm(request.GET)
        queryset = Hotel.objects.all()
        if query_form.is_valid():
            price = query_form.cleaned_data.get('price')
            category = query_form.cleaned_data.get('category')
            location = query_form.cleaned_data.get('location')
            query = Hotel.objects.filter(price=price, category__cat_name=category, location__location_name=location)
            return render(request, 'frontend/filter.html', {'queryset': query, 'queryf': query_form})
        else:
            price = query_form.cleaned_data.get('price')
            cat_id = query_form.cleaned_data.get('category')
            location = query_form.cleaned_data.get('location')  
            query = Hotel.objects.filter(location_name=location, price=price, cat_id=cat_id)
            return render(request, 'frontend/filter.html', {'queryset': query, 'queryf': query_form})
    else:
        query_form = FilterForm()
    return render(request, 'frontend/filter.html', {'queryf':query_form})

