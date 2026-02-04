"""
URL configuration for mainapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings  
from django.conf.urls.static import static  
from django.contrib import admin
from django.urls import path
from clientapp.views import *
from AdminApp.views import *


urlpatterns = [
    path('',home,name="home"),  
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('checkout/<int:total>',checkout,name="checkout"),
    path('proceedtocheckout/',proceedtocheckout,name="proceedtocheckout"),
    path('shop/',shop,name="shop"),
    path('singleproducts/<int:id>',singleproducts,name="singleproducts"),
    path('change_order_status/<int:id>', change_order_status, name="change_order_status"),
    path('delete_cart_item/<int:id>',delete_cart_item,name="delete_cart_item"),
    path('shoppingcart/',shoppingcart,name="shoppingcart"),
    path('add_to_cart/',add_to_cart,name="add_to_cart"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
    path('login_user/',login_user,name="login_user"),
    path('signup/',signup,name="signup"),
    path('add_new_user/',add_new_user,name="add_new_user"),
    # user profile
    path('profile/', user_profile, name='user_profile'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    #categoryproducts
    path('category/<int:id>', category,name="category"),
    path('category_products/<int:category_id>/', category_products, name='category_products'),
    #Tryon app
     path('tryon/<int:id>', tryon, name='tryon'),
    path('upload/', upload_image, name='upload_image'),
    #search items on client side 
    path('search_items', search_items , name="search_items"),
    path('update_cart_item/', update_cart_item, name='update_cart_item'),
    # confirmation message
    path('confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
   
   #   game 
    path('game/',game, name= "game"),
    path('submit_score/',submit_score, name='submit_score'),
    path('high_scores/', high_scores, name='high_scores'),  # Add this line

   
    #   admin path

    # Admin login URL paths
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-login-user/', admin_login_user, name='admin_login_user'),

    path('dashboard/',dashboard,name="dashboard"),
    path('dashboardprofile/',dashboardprofile,name="dashboardprofile"),
    path('update_profile/',update_profile,name="update_profile"),
    path('dashboardproduct/',dashboardproduct,name="dashboardproduct"),
    path('viewCatProducts/<int:id>',viewCatProducts,name="viewCatProducts"),
    path('add_products/',add_products,name="add_products"),
    path('deleteProduct/<int:id>',deleteProduct,name="deleteProduct"),
    path('dashboardcustomers/',dashboardcustomers,name="dashboardcustomers"),
    path('dashboardorders/',dashboardorders,name="dashboardorders"),
    path('dashboardcategories/',dashboardcategories,name="dashboardcategories"), 
    path('add_category/',add_category,name="add_category"),
    path('deletecategory/<int:id>',deletecategory,name="deletecategory"),
    path('update_category/',update_category,name="update_category"), 
    path('update_products/',update_products,name="update_products"), 
    path('deleteUser/<int:id>',deleteUser,name="deleteUser"),
    path('UpdateRecords/<int:id>',UpdateRecords,name="UpdateRecords"),  
#    search 
    path('search/', search_results, name='search_results'),

# payment gateway
path('process_payment/', process_payment, name='process_payment'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)