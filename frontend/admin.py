from django.contrib import admin
from frontend.models import Category, UserProfile, About, Hotel, Blog, Comment, BlogCategory, Signup, Review, Location, Profile


# Register your models here.
admin.site.site_header = 'HOTEL LISTING DESIGN'
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Hotel)
admin.site.register(About)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(BlogCategory)
admin.site.register(Signup)
admin.site.register(Review)
admin.site.register(Location)
admin.site.register(Profile)





