from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import News, Tickets, Merchandise,Album,Cart,CartItem
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.


def home(request):
    news_items = News.objects.order_by('-date_posted')  # latest news first
    return render(request, 'index.html', {'news_items': news_items})


def details(request):
    return render(request, 'details.html')



def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view your cart.")
        return redirect('login')

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    total_price = sum(
        (item.ticket.price if item.ticket else 0) +
        (item.merchandise.price if item.merchandise else 0) +
        (item.album.price if item.album else 0)
        for item in cart_items
    )

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total_price})

def cart_delete_item(request, item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        messages.success(request, "Item has been removed from your cart.")
    
    return redirect('cart')

def tickets(request):
    tickets_items = Tickets.objects.order_by('-date_posted')

    # Add item to cart
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        if ticket_id:
            try:
                ticket = Tickets.objects.get(id=ticket_id)
                # Get or create a cart for the user
                cart, created = Cart.objects.get_or_create(user=request.user)

                # Check if the item already exists in the cart
                cart_item, item_created = CartItem.objects.get_or_create(
                    cart=cart, ticket=ticket,
                    defaults={'quantity': 1}  # Set default quantity if new item
                )

                if not item_created:
                    # If the item exists, increase the quantity
                    cart_item.quantity += 1
                    cart_item.save()

                messages.success(request, f"Ticket '{ticket.description}' added to cart.")
            except Tickets.DoesNotExist:
                messages.error(request, "Invalid ticket ID.")

    return render(request, 'tickets.html', {'tickets_items': tickets_items})


def merchandise(request):
    merchandise_items = Merchandise.objects.order_by('-date_posted')

    if request.method == 'POST':
        merchandise_id = request.POST.get('merchandise_id')
        if merchandise_id:
            try:
                merchandise = Merchandise.objects.get(id=merchandise_id)
                # Get or create a cart for the user
                cart, created = Cart.objects.get_or_create(user=request.user)

                # Check if the item already exists in the cart
                cart_item, item_created = CartItem.objects.get_or_create(
                    cart=cart, merchandise=merchandise,
                    defaults={'quantity': 1}
                )

                if not item_created:
                    cart_item.quantity += 1
                    cart_item.save()

                messages.success(request, f"Merchandise '{merchandise.description}' added to cart.")
            except Merchandise.DoesNotExist:
                messages.error(request, "Invalid merchandise ID.")

    return render(request, 'merchandise.html', {'merchandise_items': merchandise_items})



def album(request):
    album_items = Album.objects.order_by('-date_posted')

    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        if album_id:
            try:
                album = Album.objects.get(id=album_id)
                # Get or create a cart for the user
                cart, created = Cart.objects.get_or_create(user=request.user)

                # Check if the item already exists in the cart
                cart_item, item_created = CartItem.objects.get_or_create(
                    cart=cart, album=album,
                    defaults={'quantity': 1}
                )

                if not item_created:
                    cart_item.quantity += 1
                    cart_item.save()

                messages.success(request, f"Album '{album.description}' added to cart.")
            except Album.DoesNotExist:
                messages.error(request, "Invalid album ID.")

    return render(request, 'album.html', {'album_items': album_items})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Tickets, id=ticket_id)

    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, ticket=ticket,
            defaults={'quantity': 1}
        )

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"'{ticket.description}' added to cart!")
        return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'ticket_detail.html', {'ticket': ticket})


def merchandise_detail(request, merchandise_id):
    merchandise = get_object_or_404(Merchandise, id=merchandise_id)

    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, merchandise=merchandise,
            defaults={'quantity': 1}
        )

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"'{merchandise.description}' added to cart!")
        return redirect('merchandise_detail', merchandise_id=merchandise.id)

    return render(request, 'merchandise_detail.html', {'merchandise': merchandise})

def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, album=album,
            defaults={'quantity': 1}
        )

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"'{album.description}' added to cart!")
        return redirect('album_detail', album_id=album.id)

    return render(request, 'album_detail.html', {'album': album})


def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to checkout.")
        return redirect('login')

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    total_price = sum(
        (item.ticket.price if item.ticket else 0) +
        (item.merchandise.price if item.merchandise else 0) +
        (item.album.price if item.album else 0)
        for item in cart_items
    )

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total_price
    })



def wishlist(request):
    return render(request, 'wishlist.html')


# Signup Page
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

# Login Page
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # or 'home' depending on your preference

#admin 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def admin_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin_login')
    else:
        form = UserCreationForm()
    return render(request, 'admin_signup.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_panel')
        messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

@login_required
def admin_panel(request):
    return render(request, 'admin_panel.html')


@login_required
def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        image = request.FILES['image']
        date_posted = request.POST['date_posted']
        News.objects.create(title=title, category=category, image=image, date_posted=date_posted)
        messages.success(request, 'News item added successfully.')
        return redirect('admin_panel')
    return render(request, 'add_news.html')


@login_required
def add_ticket(request):
    if request.method == 'POST':
        description = request.POST['description']
        image = request.FILES['image']
        date_posted = request.POST['date_posted']
        price = request.POST['price']
        status = request.POST['status']
        Tickets.objects.create(description=description, image=image, date_posted=date_posted, price=price, status=status)
        messages.success(request, 'Ticket added successfully.')
        return redirect('admin_panel')
    return render(request, 'add_ticket.html')


@login_required
def add_merchandise(request):
    if request.method == 'POST':
        description = request.POST['description']
        image = request.FILES['image']
        date_posted = request.POST['date_posted']
        price = request.POST['price']
        status = request.POST['status']
        Merchandise.objects.create(description=description, image=image, date_posted=date_posted, price=price, status=status)
        messages.success(request, 'Merchandise added successfully.')
        return redirect('admin_panel')
    return render(request, 'add_merchandise.html')


@login_required
def add_album(request):
    if request.method == 'POST':
        description = request.POST['description']
        image = request.FILES['image']
        date_posted = request.POST['date_posted']
        price = request.POST['price']
        status = request.POST['status']
        Album.objects.create(description=description, image=image, date_posted=date_posted, price=price, status=status)
        messages.success(request, 'Album added successfully.')
        return redirect('admin_panel')
    return render(request, 'add_album.html')
