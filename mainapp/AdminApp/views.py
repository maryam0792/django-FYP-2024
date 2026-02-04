from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import re
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from clientapp.models import *

# Create your views here.

# View to display the admin login page
def admin_login(request):
    return render(request, "admin_login.html")

# View to handle admin login form submission
def admin_login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, password=password)
            if user.type == "Admin":  # Check if the user is an admin
                request.session['id'] = user.id
                request.session['type'] = user.type
                return redirect("/dashboard")
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
                return redirect('admin_login')  # Redirect back to admin login if not admin
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('admin_login')
    return redirect('admin_login')

def dashboard(request):
    return render(request,"dashboard.html")

def dashboardprofile(request):
    if 'id' not in request.session or request.session.get('type') != 'Admin':
        return redirect('admin_login')  # Redirect to admin login if not authenticated or not admin

    user_id = request.session['id']
    user = User.objects.get(id=user_id)
    
    return render(request, "profile.html", {"user": user})

def dashboardproduct(request):
    return render(request,"product.html")

def dashboardcustomers(request):
    user=User.objects.all()
    return render(request,"customers.html",{"user":user})

def deleteUser(request,id):
    member=User.objects.get(id=id)
    member.delete()
    messages.success(request, _('Customer successfully deleted!'))
    return redirect('/dashboardcustomers')

def UpdateRecords(request, id):
    member = User.objects.get(id=id)
    if member.status == "Active":
        member.status = 'Blocked'
        messages.success(request, f'{member.fullname} successfully Blocked!')

    else:
        member.status = 'Active'
        messages.success(request, f'{member.fullname} successfully Active Now!')
    member.save()  # Ensure this is outside of the if-else block but still within the function
    return redirect('/dashboardcustomers')

def change_order_status(request, id):
    member = Order.objects.get(id=id)
    if member.status=="pending":
        member.status="dispatched"
        messages.success(request,_('Order status has been channged to dispatch.'))
    else:
       member.status="Completed"
       messages.success(request,_('Order status has been channged to dispatch.'))
    member.save()  # Ensure this is outside of the if-else block but still within the function
    return redirect('/dashboardorders')

def dashboardorders(request):
    orders=Order.objects.all()
    orderitems=OrderItem.objects.all()
    return render(request,"order.html",{"orders":orders,"orderitems":orderitems})

def dashboardcategories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html',{'categories':categories})

def add_category(request):
     # Check if the request is a POST request and contains a file
    if request.method == 'POST' and request.FILES['file']:
        # Retrieve the 'title' from the POST data
        title=request.POST.get("title")
        # Retrieve the uploaded file from the request
        file=request.FILES['file']
        # Instantiate FileSystemStorage to handle file storage
        fs = FileSystemStorage()
        Upload_File_Url=fs.url(file)
        image=file
        Category.objects.create(title=title,image=image)
        messages.success(request, _('Category successfully added!'))
    return redirect('/dashboardcategories')

def deletecategory(request,id):
    member= Category.objects.get(id=id)
    member.delete()
    messages.success(request, _('Category successfully deleted!'))
    return redirect('/dashboardcategories')

def update_category(request):
    if request.method=='POST':              # Check if the request method is POST       
        id=request.POST.get("id")           # Get the category ID from the POST data   
        member=Category.objects.get(id=id)    # Retrieve the Category object with the given ID
        title = request.POST.get("title")      # Get the title from the POST data and update the category's title
        member.title= title
    if bool(request.FILES.get('file',False)) == True:    # Check if a file has been uploaded
            file=request.FILES['file']                   # Get the uploaded file from the request
            fs=FileSystemStorage()                       # Create a FileSystemStorage instance
            Upload_File_Url=fs.url(file)                 # Get the URL for the uploaded file
            image=file                                   # Set the uploaded file as the category's image
            member.image=image                           # Save the updated category object to the database
            member.save()
            messages.success(request, _('Category successfully updated!'))
    return redirect('/dashboardcategories')

def update_profile(request):
    if request.method == 'POST':
       id=request.session['id']
       user=User.objects.get(id=id)
       fullname=request.POST.get("fullname")
       email=request.POST.get("email")
       email_pattern = r'^[\w\.-]+@gmail\.com$'
       if not re.match(email_pattern, email):
            messages.error(request, "Please enter a valid Gmail address (e.g., name@gmail.com).")
            return redirect ("/dashboardprofile")
       password=request.POST.get("password")
       address=request.POST.get("address")
       type=request.POST.get("type")
       user.fullname=fullname
       user.email=email
       user.password=password
       user.address=address
       user.type=type
       if bool(request.FILES.get('file',False)) == True:
         file=request.FILES['file']
         fs=FileSystemStorage()
         Upload_File_Url=fs.url(file)
         image=file
         user.image=image
    user.save()     
    return redirect('/dashboardprofile')

def update_products(request):
    if request.method=='POST':
     #get the product form data
     id=request.POST.get("id")
     title=request.POST.get("title")
     price=request.POST.get("price")
     description=request.POST.get("description")
     member=Product.objects.get(id=id)
     # Update the product fields
     member.title=title
     member.price=price
     member.description=description
     # Update the main image
     if bool(request.FILES.get('file',False)) == True:
         file=request.FILES['file']
         fs=FileSystemStorage()
         Upload_File_Url=fs.url(file)
         image=file
         member.image=image
    # Update the tryon image
     if bool(request.FILES.get('tryonfile', False)) == True:
         file=request.FILES['tryonfile']
         fs=FileSystemStorage()
         Upload_File_Url=fs.url(file)
         tryon=file
         member.tryon=tryon
     # Save the updated product    
    member.save()         
    return redirect('/dashboardcategories')

def viewCatProducts(request, id):
    cat=Category.objects.get(id=id)
    Products=Product.objects.filter(category=cat)   #this category is define in models.py 
    catId=id
    return render(request,"product.html",{"Products":Products,"catId":catId})

def add_products(request):
    if request.method =='POST' and request.FILES['file'] and request.FILES['tryonfile']:
        catId=request.POST.get("catId")
        title=request.POST.get("title")
        price=request.POST.get("price")
        description=request.POST.get("description")
        #main image  file upload
        file=request.FILES['file']
        fs=FileSystemStorage()
        Upload_file_Url=fs.url(file)
        image=file
        #virtual tryon image  file upload
        file=request.FILES['tryonfile']
        fs=FileSystemStorage()
        Upload_file_Url=fs.url(file)
        tryon=file
        category=Category.objects.get(id=catId)
        Product.objects.create(title=title,price=price,description=description,image=image,tryon=tryon,category=category)
        messages.success(request, _('Product successfully added!'))
    return redirect('/dashboardcategories')

def deleteProduct(request, id):
    member=Product.objects.get(id=id)
    member.delete()
    messages.success(request, _('Successfuly delete product !'))
    return redirect('/dashboardcategories')


# product searching 

def search_results(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    # Debugging lines
    print(f"Query: {query}, Category ID: {category_id}, From: {from_date}, To: {to_date}")

    # Start with all products
    products = Product.objects.all()

    # Apply query filter if any
    if query:
        products = products.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    # Apply category filter if any
    if category_id:
        products = products.filter(category_id=category_id)

    # Apply date range filter if both dates are provided
    if from_date and to_date:
        products = products.filter(created_at__range=[from_date, to_date])

    # Debugging line to check filtered products
    print(f"Filtered Products: {products}")

    # Get all categories for the dropdown in the search form
    categories = Category.objects.all()

    # Prepare the context with products and categories
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(request, 'search_results.html', context)

from django.views.decorators.http import require_POST
from django.http import JsonResponse
def process_payment(request):
    fullname = request.POST.get('fullname')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    area = request.POST.get('area')
    areacode = request.POST.get('areacode')
    total = request.POST.get('total')

    # Here, you can process the payment or store the order in the database
    # For demonstration, we'll just return a success message
    response_data = {
        'message': 'Payment processed successfully!',
        'total': total
    }

    return JsonResponse(response_data)
