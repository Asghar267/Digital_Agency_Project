from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Customer, Order, Cart, Service
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail


def search(request):
    search_term = request.GET.get('q')
    print("search_term: ", search_term)
    if not search_term:
        services = Service.objects.all()
    else:
        # services = Service.objects.filter(product_name__icontains=search_term)
        services = Service.objects.filter(service_title__icontains=search_term)

    return render(request, 'service_list.html', {'services': services, 'search_term': search_term})


def register_user(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        print("username:", username)
        print("password1:", password)
        print("confirm_password:", confirm_password)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect(register_user)

        user = User.objects.create_user(
            first_name=full_name, username=username, email=email, password=password)
        user.save()
        messages.success(
            request, "Registration successful. You can now log in.")

        # print("Field Error:", field.name,  field.errors) # debugging
        # print("Form Error:", form.errors)

        # Send email to the customer with order details
        order_details = f"Mr/Mrs. {full_name},\n"
        order_details += f"\nThank you for registering with our website! We are excited to have you as a new member of our community.\n\nYour registration details are as follows:"
        order_details += f"\nUsername: {username}\nEmail: {email}" 
        order_details += f"\n\nPlease keep this information safe for your records. \nYou can now log in to our website using your registered credentials and explore all the features and benefits we offer."
        order_details += f"\n\nBest regards,\nAsghar Abbasi"
        order_details += f"\n\nLinkedIn: https://www.linkedin.com/in/asghar267/"
        
        # send_mail(
        #     'Registration Confirmation',
        #     order_details,
        #     'asgharabbasikalhoro@gmail.com',  # Replace with your email address
        #     [email],  # Send email to the customer's email address
        #     fail_silently=False,
        # )
        
        # print(f"register {username} email sent to {email}")
        return redirect('login_user')

    context = {"form": form}
    return render(request, "register.html", context)


def loginUser(request):
    if request.method == "POST":
        username1 = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            next_param = request.GET.get('next')
            if next_param and next_param != "/signin/":
                print("next_param:", next_param)
                return redirect(next_param)
            else:
                # Replace 'home' with the appropriate URL name for the default page
                return redirect(reverse('service_list'))
        else:
            messages.info(request, "Username or Password is incorrect!")
            return render(request, "login.html")

    return render(request, "login.html")


@login_required(login_url='login_user')
def logoutUser(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def profileUser(request):
    print('request.user :', request.user)
    print('request.user att :', request.user.is_authenticated)
    user = User.objects.filter(username=request.user)
    order = Order.objects.filter(customer=request.user)
    print(user)
    print("order :", order)
    return render(request, "profile.html", {'user': user, 'order': order})

@login_required(login_url='login_user')
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})


def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'service_detail.html', {'service': service})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = Order.objects.filter(order=order)
    # order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})


# session based
def add_to_cart(request, service_id):
    quantity =  1
    # print("Quantity:", quantity)
    service = Service.objects.get(pk=service_id)
    cart_item = {
        'service_id': service_id,
        'quantity': int(quantity),
    }

    if request.session.get('cart'):
        cart = request.session['cart']
        if service_id in cart:
            cart[service_id]['quantity'] = int(quantity)
        else:
            cart[service_id] = cart_item
        request.session.modified = True
    else:
        cart = {
            service_id: cart_item
        }
        request.session['cart'] = cart

    messages.success(request, 'Item added successfully!')
    print(messages)

    return redirect('service_list')


# session  based
def cart(request):
    if request.method == 'POST':
        user_r = request.user
        cart_items = Cart.objects.filter(user=user_r)
        # Create a new Cart object for each item in the cart
        cart = request.session.get('cart', {})
        for item in cart.values():
            service = get_object_or_404(Service, pk=item['service_id'])
            total_price = service.price *1
            cart_item, created = Cart.objects.get_or_create(
                user=request.user, service=service)
            order = Order.objects.create(customer=user_r, orderitem=cart_item,
                                         total_price=total_price, status="pending")
            order.save()
            service.save()
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()

        # Send email to the customer with order details
        order_details = f"Mr/Mrs: {user_r.username} \n\nYour Order details \nOrder ID: {order.id}\n\n"
        order_details += "Order Items:\n"
        for item in cart.values():
            service = Service.objects.get(pk=item['service_id'])
            order_details += f"\nProduct: {service.service_title},\nQuantity: {item['quantity']}, Price:{service.price}, Total:{ service.price * item['quantity']} \n"
        order_details += "\n\nThanks For Purchasing."
        order_details += f"\n\nBest regards,\nAsghar Abbasi"
        order_details += f"\n\nLinkedIn: https://www.linkedin.com/in/asghar267/"
        # send_mail(
        #     'Order Confirmation',
        #     order_details,
        #     'asgharabbasikalhoro@gmail.com',  # Replace with your email address
        #     [user_r.email],  # Send email to the customer's email address
        #     fail_silently=False,
        # )

        # Clear the cart in the session
        request.session['cart'] = {}
        messages.success(request, 'Your order has been placed!')
        return redirect('service_list')

    # Display the items in the cart
    cart_items = []
    cart = request.session.get('cart', {})
    for item in cart.values():
        service = Service.objects.get(pk=item['service_id'])
        cart_items.append({'service': service, 'quantity': item['quantity']})

    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)


def remove_from_cart(request, service_id):
    print("rem :", service_id)

    service_id = str(service_id)
    cart = request.session.get('cart', {})

    print(cart)
    if service_id in cart:
        print("  if service_id in cart: ", service_id in cart)
        del cart[service_id]
        request.session['cart'] = cart
    return redirect('cart')
