import json
import calendar
from http.client import responses

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count, Case, IntegerField, When
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView
from django.views.generic import ListView
from .models import Type, Item, LabMember, OrderItem
from .forms import OrderItemForm, InterestForm


# Index View: Displaying Types (up to 10) in the Template
# For the index view:
# YES, passing 'type_list' as extra context variable
# 'type_list' contains the list of types to display on the index page.

# views.py
from django.shortcuts import render


def index(request):
    # Implement session counter
    if 'session_counter' in request.session:
        request.session['session_counter'] += 1
    else:
        request.session['session_counter'] = 1

    # Display item types if the user is authenticated
    type_list = Type.objects.all().order_by('id')[:10] if request.user.is_authenticated else None

    # Render response with context data, including the session counter and item types
    response = render(request, 'index.html', {
        'session_counter': request.session['session_counter'],
        'type_list': type_list,
        'user': request.user
    })

    # Set a cookie named 'recent_visit' with a 10-second expiry if not already set
    if not request.COOKIES.get('recent_visit'):
        response.set_cookie('recent_visit', 'true', max_age=10)

    return response


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('myapp:login')  # Redirect to login page after signup
    template_name = 'signup.html'

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('myapp:index')  # Redirect to the main page after successful login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

# For the about view:
# NO, no extra context variables are required.
# Only a message variable is passed to render the welcome message.
# if required we can pass year and month its an optional argument
def about(request, year=None, month=None):
    if year and month:
        month_name = calendar.month_name[month]
        message = f"Welcome to our Online Grocery Store for {month_name} {year}."
    else:
        message = "Welcome to our Online Grocery Store."
    return render(request, 'about.html', {'message': message})

@login_required
def myorders(request):
    # Check if the logged-in user is a client
    if hasattr(request.user, 'client'):  # Checks if the user is a Client instance
        # Fetch all orders for this client
        orders = OrderItem.objects.filter(client=request.user.client)
        return render(request, 'myorders.html', {'orders': orders})
    else:
        # Display message if the user is not a registered client
        return render(request, 'myorders.html', {'message': 'You are not a registered client!'})

# Detail View: Displaying Items for a Specific Type
# For the detail view:
# YES, passing 'selected_type' and 'items' as extra context variables.
# 'selected_type' represents the specific type being viewed.
# 'items' contains the list of items for the selected type.
def detail(request, type_no):
    selected_type = get_object_or_404(Type, pk=type_no)
    items = Item.objects.filter(type=selected_type)
    # YES, passing 'selected_type' and 'items' as extra context variables
    return render(request, 'detail.html', {'selected_type': selected_type, 'items': items})


# Class-Based View for Displaying User List
class Usercbv(ListView):
    model = User
    template_name = 'user_list.html'  # Specifying the template for CBV

    def get_queryset(self):
        # Ordering users by username
        return User.objects.all().order_by('username')


# views.py



class LabGroupView(ListView):
    model = LabMember
    template_name = 'lab_group.html'  # Template to render the lab group members list
    context_object_name = 'members'

    def get_queryset(self):
        return LabMember.objects.all().order_by('-first_name')  # Order by first name descending


def items(request):
    # Annotate each item with a count of interested users, only if there are actual interests
    itemlist = Item.objects.annotate(
        interested_count=Count(
            Case(
                When(interested__isnull=False, then=1),  # Count only when interested entries exist
                output_field=IntegerField()
            )
        )
    ).order_by('id')[:20]
    return render(request, 'items.html', {'itemlist': itemlist})

def placeorder(request):
    return HttpResponse("You can place your order here.")


# View for displaying the OrderItem form
def place_order(request):
    form = OrderItemForm()
    return render(request, 'place_order.html', {'form': form})


def show_interest(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']
            quantity = form.cleaned_data['quantity']
            comments = form.cleaned_data['comments']

            # Update the interested count based on user input
            if interested == '1':  # Check if user selected "Yes"
                item.interested += 1
                item.save()

            # Optionally, handle quantity and comments if needed

            return redirect('myapp:items')  # Redirect to items list after submitting the form

    else:
        form = InterestForm()

    return render(request, 'show_interest.html', {'form': form, 'item': item})