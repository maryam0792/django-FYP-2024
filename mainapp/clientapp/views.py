from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import UploadImageForm
from django.core.paginator import Paginator
from PIL import Image
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages


# for tryon feature
def tryon(request,id):
    product=Product.objects.get(id=id)
    Products=Product.objects.filter(category=product.category)  #used to show related products on singleproduct page
    form = UploadImageForm()
    return render(request, 'tryonapp/upload.html', {'form': form,"product":product,"Products":Products})

def upload_image(request):
    if request.method == 'POST':
        id=request.POST.get("id")
        product=Product.objects.get(id=id)
        Products=Product.objects.filter(category=product.category)  #used to show related products on singleproduct page
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            messages.success(request, 'Image uploaded successfully!')
            return render(request, 'tryonapp/upload.html', {
                'form': form,
                'uploaded_file_url': uploaded_file_url,
                "product":product
            })
    else:
        form = UploadImageForm()
    return render(request, 'tryonapp/upload.html', {'form': form,"product":product,"Products":Products})
# end of tryon feature


# game
def game(request):
    # Check if user is logged in via session
    if not request.session.get('id'):  # Assuming 'id' is the session key for user login
        return redirect('/login/')  # Redirect to login page if not logged in
    return render(request,"game/game.html")

def submit_score(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                score = int(request.POST.get('score', 0))
                new_score = PlayerScore(user=user, score=score)
                new_score.save()
                # for coins  
                 # Update user's coins and rupees
                user_currency, created = UserCurrency.objects.get_or_create(user=user)
                user_currency.update_coins_and_rupees(score)   


                return JsonResponse({'status': 'success'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'fail'}, status=400)
        return JsonResponse({'status': 'fail'}, status=400)
    return JsonResponse({'status': 'fail'}, status=400)

def high_scores(request):
    # Retrieve the top scores, ordered by highest score first
    scores = PlayerScore.objects.order_by('-score')[:10]  # Get top 10 scores
    return render(request, 'game/high_scores.html', {'scores': scores})

# Create your views here.
def home(request):
    Products=Product.objects.all()       # Retrieve all product entries from the database
    categories=Category.objects.all()     # Retrieve all category entries from the database
    recent_date = timezone.now() - timedelta(days=1)
    new_arrivals = Product.objects.filter(created_at__gte=recent_date)
    print("New Arrivals:", new_arrivals) 
    return render(request,"index.html",{"Products":Products,"categories":categories, 'new_arrivals': new_arrivals})


def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def login(request):
    return render(request,"login.html")

def login_user(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user=User.objects.get(email=email,password=password)
            request.session['id']=user.id
            request.session['type']=user.type
            if user.type == "customer":
                return redirect("/")
            if user.type == "Admin":
                return redirect("/dashboard")
        except user.DoesNotExist:
            return redirect("login")

def logout(request):
    del request.session['id']
    del request.session['type']
    return redirect('login')        

def signup(request):
    return render(request,"signup.html")

def user_profile(request):
    """View to display the user's profile."""
    if 'id' not in request.session:
        return redirect('login')  # Redirect to login if not authenticated

    user_id = request.session['id']
    try:
        user = User.objects.get(id=user_id)
        if user.type != 'customer':
            return redirect('login')  # Redirect if not a customer
        
        # Retrieve the user's game scores
        # scores = PlayerScore.objects.filter(user=user).order_by('-score')
        # Retrieve the latest game score
        latest_score = PlayerScore.objects.filter(user=user).order_by('-date_recorded').first()
        

        # Retrieve the user's currency details
        user_currency, created = UserCurrency.objects.get_or_create(user=user)

        context = {
            'user': user,
            'latest_score': latest_score,
            'coins': user_currency.coins,
            'rupees': user_currency.rupees,

        }
        return render(request, 'user_profile.html', context)
    except User.DoesNotExist:
        return redirect('login')  # Redirect to login if the user is not found

def edit_profile(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')  # Redirect to login if the user is not authenticated

    user = User.objects.get(id=user_id)

    # Ensure only customers can update this profile
    if not user.is_customer():
        return redirect('dashboarprofile')

    if request.method == "POST":
        user.fullname = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.address = request.POST.get('address')
        user.image = request.FILES.get('image', user.image)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'edit_profile.html', {'user': user})

def add_new_user(request):
    if request.method=='POST':
        fullname=request.POST.get("fullname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            # Validate that the fullname contains only alphabetic characters
            validate_alphabetic(fullname)
            user=User(fullname=fullname,email=email,password=password,address=address)
            user.save()
            return redirect("login")
        except ValidationError as e:
            # If validation fails, show an error message
            return render(request, 'signup.html', {'error': e.message})

    return render(request, 'signup.html')    

def validate_alphabetic(value):
    if not value.isalpha():
        raise ValidationError(
            _('Name should only contain alphabetic characters (a-z, A-Z).'),
            params={'value': value},
        )

def shop(request):
    # Fetch all products
    products = Product.objects.all()
    categories = Category.objects.all() # Retrieve all categories
    # Pagination
    paginator = Paginator(products, 6)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_result = page_obj.start_index()
    end_result = page_obj.end_index()
    total_results = paginator.count
    
   

    return render(request, 'shop.html', {
        'products': page_obj,
        'categories': categories,
        'page_object':page_obj,
        'start_result': start_result,
        'end_result': end_result,
        'total_results': total_results
        # 'current_page': page_obj.number,
        # 'num_pages': paginator.num_pages,
    })
    
def singleproducts(request,id):
        product=Product.objects.get(id=id)
        Products=Product.objects.filter(category=product.category)  #used to show related products on singleproduct page
        return render(request,"singleproducts.html",{"product":product,"Products":Products})

def shoppingcart(request):
    if request.session.get('id',None):
        c_id=request.session['id']
        customer=User.objects.get(id=c_id)
        items=Cart.objects.filter(customer=customer)
        total=0
        for item in items:
            total = total + (item.product.price * item.quantity)     #calculate the total amount
        # Check if the cart is empty
        is_empty = not items.exists()  # True if the cart is empty
        
        if is_empty:
            messages.info(request, 'Your cart is empty. Add items to your cart to proceed.')
            
        return render(request,"shoppingcart.html",{"items":items,"total":total,"is_empty": is_empty })
    else:
        return redirect("login")

def checkout(request,total):
    if request.session['id']:
        c_id=request.session['id']
        customer=User.objects.get(id=c_id)
        items=Cart.objects.filter(customer=customer)
        # Fetch user currency details
        user_currency, created = UserCurrency.objects.get_or_create(user=customer)


                # Subtract the coins from the total
        rupees_to_deduct = user_currency.rupees
        adjusted_total = total - rupees_to_deduct

        # Ensure the adjusted total doesn't go negative
        if adjusted_total < 0:
            adjusted_total = 0
        

        return render(request,"checkout.html",{"items":items,"total":total, "adjusted_total": adjusted_total,"coins": user_currency.coins,
            "rupees": user_currency.rupees,})
    else:
        return redirect("login")
    
def proceedtocheckout(request):
    if request.session.get('id', None):
        c_id = request.session['id']
        customer = User.objects.get(id=c_id)  # Read customer
        items = Cart.objects.filter(customer=customer)

        # Read customer details
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        area = request.POST.get("area")
        areacode = request.POST.get("areacode")
        bill = request.POST.get("bill")

        # Convert 'bill' to a numeric value (int or float)
        try:
            bill = float(bill)  # You can also use `int(bill)` if it's an integer
        except ValueError:
            return render(request, "error.html", {"message": "Invalid bill value."})

        status = "pending"

        # Fetch user currency details
        user_currency, created = UserCurrency.objects.get_or_create(user=customer)

        # Apply coins if available and sufficient
        discount = 0
        if user_currency.coins >= 200:
            discount = user_currency.redeem_coins(bill)  # Calculate discount and update coins
            final_bill = bill - discount
        else:
            final_bill = bill

        # Save the order with the final bill amount
        order = Order(
            bill=final_bill,  # Save the final amount after discount
            fullname=fullname,
            phone=phone,
            address=address,
            city=city,
            area=area,
            areacode=areacode,
            status=status,
            customer=customer
        )
        order.save()

        # Save the order items
        for item in items:  # Items read from the cart
            orderitem = OrderItem(quantity=item.quantity, product=item.product, order=order)
            orderitem.save()

        # Delete items from the cart after saving them to the order
        for item in items:
            cart = Cart.objects.get(id=item.id)
            cart.delete()

        return redirect('order_confirmation', order_id=order.id)
    else:
        return redirect("login")

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def add_to_cart(request):
    if request.method=='POST' and request.session.get('id',None):
        quantity=request.POST.get("quantity")
        p_id=request.POST.get("product")             #get product
        product=Product.objects.get(id=p_id)    #find the specific product id
        c_id=request.session['id']
        customer=User.objects.get(id=c_id)
        # cart=Cart(quantity=quantity,product=product,customer=customer)
        # cart.save()

      # Check if the item is already in the cart
        cart, created = Cart.objects.get_or_create(
            product=product,
            customer=customer,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart.quantity += int(quantity)
            cart.save()
        
        # Get updated cart item count
        item_count = Cart.objects.filter(customer=customer).count()

        return redirect("/shoppingcart",{'item_count': item_count})
    else:
        return redirect("/login")

def update_cart_item(request):
    if request.method == 'POST' and request.session.get('id', None):
        item_id = request.POST.get("item_id")
        new_quantity = int(request.POST.get("quantity"))

        cart_item = Cart.objects.get(id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        
        return redirect("/shoppingcart")
    else:
        return redirect("/login")

def delete_cart_item(request,id):
    if request.session.get('id',None):
       item=Cart.objects.get(id=id)
       item.delete()
       return redirect("/shoppingcart")
    else:
        return redirect("login")
# views.py in clientside app
def category(request,id):
    products=Product.objects.filter(category=id)            # Retrieve products that belong to the specified category using the category id.
    categories=Category.objects.all()                       # Retrieve all categories from the database.
    return render(request,"shop.html",{"products":products,"categories":categories})

def category_products(request, category_id=None):
    if category_id:
       category = Category.objects.get(id=category_id)                          # Get the category object using the provided category_id
       products = Product.objects.filter(category=category).order_by("id")      # Filter products belonging to the specified category and order them by their id
       paginator = Paginator(products, 6)                                       # Show 6 products per page
       page_number = request.GET.get('page')                                    # Get the current page number from the request
       page_obj = paginator.get_page(page_number)                               # Get the products for the current page
    else: 
       products = Product.objects.all()                                         # If no category_id is provided, fetch all products and set category to None
       category = None
       # Calculate the starting and ending results for pagination
 
    start_result = (page_obj.number - 1) * paginator.per_page + 1
    end_result = start_result + len(page_obj.object_list) - 1
    total_results = paginator.count

     # Pagination
   

    # Retrieve specific categories
    categories = Category.objects.all()

    return render(request, 'category/category_products.html', {
        'category': category,
        'page_obj': page_obj,
        'start_result': start_result,
        'end_result': end_result,
        'total_results': total_results,
        'products': page_obj,
        'categories': categories,
        'total_products': products.count(),
        'current_page': page_obj.number,
        # 'num_pages': paginator.num_pages,
    })

# searching

def search_items(request):
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

    return render(request, 'search_items.html', context)

