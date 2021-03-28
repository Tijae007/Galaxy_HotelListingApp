from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 

from django.contrib import messages


from frontend.models import *
from backend.forms import *

from django.contrib.auth import update_session_auth_hash

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.forms import CommentForm
from backend.forms import ReviewForm
from django.db.models import Count, Q
from frontend.filters import HotelFilter

# Password Reset
from django.core.mail import send_mail, BadHeaderError
# from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from backend.forms import  PasswordReset, SetPassword


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('frontend:homepage')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'frontend/login2.html')

def login_userview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('backend:dashboard')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'frontend/userlogin.html')

@login_required(login_url='/dashboard/')
def dashboard(request):
    return render(request, 'backend/index.html')

@login_required(login_url='/user_dashboard/')
def user_dashboard(request):
    return render(request, 'backend/userindex.html')

@login_required(login_url='/dashboard/')
def logout_view(request):
    logout(request)
    return redirect('backend:login_view')

@login_required(login_url='/dashboard/')
def bookings(request):
    return render(request, 'backend/bookings.html')

@login_required(login_url='/dashboard/')
def listings(request):
    # hotel_list = Hotel.objects.order_by('-date')
    hotel_list = Hotel.objects.filter(user=request.user)
    return render(request, 'backend/listings.html', {'hlist':hotel_list})

@login_required(login_url='/dashboard/')
def new_listings(request):
    # hotel_list = Hotel.objects.order_by('-date')
    hotel_list = Hotel.objects.filter(user=request.user)
    return render(request, 'backend/newlistings.html', {'hlist':hotel_list})

def new_listings2(request):
    hotel_list = Hotel.objects.order_by('-date')
    # hotel_list = Hotel.objects.filter(user=request.user)
    return render(request, 'backend/newlistings.html', {'hlist':hotel_list})

def listings2(request):
    hotel_list = Hotel.objects.order_by('-date')
    # hotel_list = Hotel.objects.filter(user=request.user)
    return render(request, 'backend/listings.html', {'hlist':hotel_list})

@login_required(login_url='/dashboard/')
def reviews(request):
    review_list = Review.objects.filter(user=request.user)
    return render(request, 'backend/reviews.html', {'rlist':review_list})


@login_required(login_url='/dashboard/')
def add_listing(request):
    if request.method == 'POST':
        list_form = ListingForm(request.POST, request.FILES)
        if list_form.is_valid():
            listf = list_form.save(commit=False)
            listf.user = request.user
            listf.save()
            messages.success(request, 'Hotel Posted')
            
    else:
        list_form = ListingForm()
    return render(request, 'backend/add-listing.html', {'listf': list_form})

@login_required(login_url='/dashboard/')
def add_newlisting(request):
    if request.method == 'POST':
        list_form = ListingForm(request.POST, request.FILES)
        if list_form.is_valid():
            listf = list_form.save(commit=False)
            listf.user = request.user
            listf.save()
            messages.success(request, 'Hotel Posted')
    else:
        list_form = ListingForm()
    return render(request, 'backend/add-newlisting.html', {'listf': list_form})


@login_required(login_url='/dashboard/')
def user_profile(request):
    agents = UserProfile.objects.filter(user=request.user)
    return render(request, 'backend/user-profile.html', {'profile':request.user, 'agents': agents})

@login_required(login_url='/dashboard/')
def user_newprofile(request):
    agents = UserProfile.objects.filter(user=request.user)
    return render(request, 'backend/user-newprofile.html', {'profile':request.user, 'agents': agents})

@login_required(login_url='/dashboard/')
def charts(request):
    return render(request, 'backend/charts.html')

@login_required(login_url='/dashboard/')
def newcharts(request):
    return render(request, 'backend/newcharts.html')

def register_form(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            user.profile.first_name = register_form.cleaned_data.get('first_name')
            user.profile.last_name = register_form.cleaned_data.get('last_name')
            user.profile.email = register_form.cleaned_data.get('email')
             # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Galaxy Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('backend/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')

            # messages.success(request, 'User Registered')
    else:
        register_form = RegisterForm()
    return render(request, 'frontend/register.html', {'reg': register_form})


#def register_form(request):
#    if request.method == 'POST':
#        register_form = RegisterForm(request.POST)
#        if register_form.is_valid():
#            register_form.save()
#            messages.success(request, 'User Registered')
#    else:
#        register_form = RegisterForm()
#    return render(request, 'frontend/register.html', {'reg': register_form})

def pass_form(request):
    if request.method == 'POST':
        pass_form = ChangePasswordForm(data=request.POST,
        user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'Password changed successfully.')
    else:
        pass_form = PasswordChangeForm(user=request.user)
    return render(request, 'backend/pass-form.html', {'pass_key':pass_form})

def pass_newform(request):
    if request.method == 'POST':
        pass_form = ChangePasswordForm(data=request.POST,
        user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'Password changed successfully.')
    else:
        pass_form = PasswordChangeForm(user=request.user)
    return render(request, 'backend/pass-newform.html', {'pass_key':pass_form})

def edit_form(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, 'backend/edit-user-profile.html', {'edit_key':edit_form})

def edit_newform(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, 'backend/edit-newuser-profile.html', {'edit_key':edit_form})

def reset(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(data=request.POST,
        user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'Password changed successfully.')
    else:
        pass_form = PasswordChangeForm(user=request.user)
    return render(request, 'backend/reset.html', {'pass_key':pass_form})

def blog_form(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog Posted')
    else:
        blog_form = BlogForm()
    return render(request, 'backend/add-blog.html', {'blog': blog_form})

def edit_blog(request, blog_id):
    single_blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        edit_form = EditBlog(request.POST, request.FILES, instance=single_blog)
        if edit_form.is_valid():
            blogf = edit_form.save(commit=False)
            blogf.user = request.user
            blogf.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditBlog(instance=single_blog)
    return render(request, 'backend/edit-blog.html', {'edit_key':edit_form})

def edit_listing(request, hotel_id):
    single_listing = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        edit_form = EditListing(request.POST, request.FILES, instance=single_listing)
        if edit_form.is_valid():
            blogf = edit_form.save(commit=False)
            blogf.user = request.user
            blogf.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditListing(instance=single_listing)
    return render(request, 'backend/edit-listing.html', {'edit_key':edit_form})

    # def edit_blog(request, blog_id):
    # if request.method == 'POST':
    #     blog_edit = EditBlog.objects.get(pk=blog_id)
    #     blog_edit = EditBlog(request.POST or None, instance= blog_edit)
    #     if blog_edit.is_valid():
    #         blog_edit.save()
    #         messages.success(request, 'User edited successfully.')
    # else:
    #     blog_edit = EditBlog.objects.get(pk=blog_id)
    #     # edit_form = EditBlog(instance=request.user)
    # context = {
    #         # 'task_obj': task_obj, 
    #         # 'task': all_tasks,
    #         # 'edit_key':edit_form,
    #         'blog_edit':blog_edit
    # }
    # return render(request, 'backend/edit-blog', context)

def show_post(request):
    # list_blog = Blog.objects.order_by('-date')
    list_blog = Blog.objects.filter(user=request.user)
    return render(request, 'backend/view-blog.html', {'list':list_blog})

def show_post2(request):
    list_blog = Blog.objects.order_by('-date')
    # list_blog = Blog.objects.filter(user=request.user)
    return render(request, 'backend/view-blog.html', {'list':list_blog})

def delete_post(request, blog_id):
    post_record = get_object_or_404(Blog, id=blog_id)
    post_record.delete()
    return redirect('backend:show_post')

def delete_hotel(request, listf_id):
    post_record = get_object_or_404(Hotel, id=listf_id)
    post_record.delete()
    return redirect('backend:new_listings')

def delete_newhotel(request, listf_id):
    post_record = get_object_or_404(Hotel, id=listf_id)
    post_record.delete()
    return redirect('backend:listings')

def view_listingdetails(request, pk):
    post = get_object_or_404(Hotel, pk=pk)
    return render(request, 'backend/view-listing.html', {'pst':post})

def view_newlistingdetails(request, pk):
    post = get_object_or_404(Hotel, pk=pk)
    return render(request, 'backend/view-newlisting.html', {'pst':post})

def view_blogdetails(request, pk):
    single_post = get_object_or_404(Blog, pk=pk)
    return render(request, 'backend/view-blogdetail.html', {'sipst':single_post})

def about(request):
    about = About.objects.all()
    user_var = User.objects.order_by('-last_name')
    context = {'abt':about, 'user':user_var}
    return render(request, 'backend/about.html', context)

def about_detail(request, abt_id):
    detail = About.objects.get(id=abt_id)
    return render(request, 'backend/about_detail.html', {'det':detail})

def hotel(request):
    most_recent = Hotel.objects.order_by('-date')[:4]
    all_post = Hotel.objects.order_by('-date')
    paginated_filter = Paginator(all_post, 4)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filter.get_page(page_number)
    context = {
        'person_page_obj': all_post, 
        'most_recent': most_recent,
    }
    context['person_page_obj'] = person_page_obj

    return render(request, 'backend/hotels-grid-sidebar-2.html', context)


def hotel_detail(request, pk):
    post = get_object_or_404(Hotel, pk=pk)
    reviews = Review.objects.filter(post=pk).order_by('-timestamp')
    if request.method == "POST":
        Rform = ReviewForm(request.POST)
        if Rform.is_valid():
            review = Rform.save(commit=False) 
            review.post = post
            review.save()
            return redirect('backend:hotel_detail', pk=post.pk)
    else:
        Rform = ReviewForm()
    return render(request, 'backend/hotel-detail.html', {'pst':post, 'Rform':Rform, 'revs':reviews})

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

    return render(request, 'backend/blog.html', context)

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
            return redirect('backend:blog_post', pk=single_post.pk)
        #  single_post = {'form': form, 'most_recent': most_recent,}
    else:
        form = CommentForm()
    return render(request, 'backend/blog-post.html', {'comm':comments, 'form':form, 'sipst':single_post})

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
        from_email = 'From <tijaniyunus07@gmail.com>'
        send = mail.send_mail(subject, plain_message, from_email, [
                    'teezee132@gmail.com', 'tijaniyunus07@gmail.com', email], html_message=html_message, fail_silently=True)
        if send:
            messages.success(request, 'Email sent')
        else:
            messages.error(request, 'Mail not sent')

    return render(request, 'backend/contacts.html')

def post_from_cat(request, category_id):
    count_post = Hotel.objects.filter(cat_id__id=category_id).count()
    try:
        get_cat_name = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return render(request, 'frontend/404.html')
    # get_cat_name = Category.objects.get(id=category_id)
    post_cat= Hotel.objects.filter(cat_id__id=category_id)
    context = {'posts': post_cat, 'counts': count_post, 'cat': get_cat_name}
    return render(request, 'backend/post-cat.html', context)

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
    return render(request, 'backend/search_results.html', context)

def filtersearch(request):
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
    return render(request, 'backend/filter.html', context)

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordReset(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "backend/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'tijaniyunus07@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="backend/password_reset.html", context={"password_reset_form":password_reset_form})

def activation_sent_view(request):
    return render(request, 'backend/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('backend:login_view')
    else:
        return render(request, 'backend/activation_invalid.html')

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
    return render(request, 'backend/filtersearch.html', context)
