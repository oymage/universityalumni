from django.shortcuts import render, redirect
from apps.users.forms import LoginForm, RegistrationForm, EventForm, VenueForm, SpeakerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.users.models import Account, Event, Venue, Speaker, Ticket
from django.core.paginator import Paginator
import random
from django.db.models import Q
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import paypalrestsdk
from django.conf import settings

# Create your views here.
def signup(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            messages.success(request, f"Welcome {account.name}. You have successfully logged in.")
            login(request, account)
            return redirect('users:home')
        else:
            messages.error(request, "Error creating account. Please correct the highlighted errors")
    return render(request, 'signup.html', {
        'form': form,
    })

def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email', None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_short_name}.")
                return redirect('users:home')
            else:
                messages.error(request, "An error occurred. Kindly try again with correct credentials, reset password if you have forgotten or contact us.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
            messages.error(request, f"Invalid credentials. Please try again.")
    return render(request, 'signin.html', {
        'form': form,
    })

def forgot_password(request):
    return render(request, 'forgot-password.html', {
        'page': 'forgot',
    })

def logout_user(request):
	if request.user.is_authenticated:
		username = request.user.name
		logout(request)
		messages.info(request, f"{username} has been logged out.")
	else:
		messages.warning(request, "No user is currently logged in.")
	return redirect('users:home')

def home(request):
    all_users = Account.objects.all()
    total_users = str(all_users.count()).zfill(3)
    total_speakers = str(random.randint(1, 10)).zfill(3)
    total_events = str(12).zfill(3)
    total_tickets = str(random.randint(20, 30)).zfill(3)
    total_male = all_users.filter(gender='male').count()
    total_female = all_users.filter(gender='female').count()
    total_other = all_users.filter(gender='other').count()
    upcoming_events = Event.objects.all().order_by('-date')[:3]
    return render(request, 'dashboard.html', {
        'total_users': total_users,
        'total_speakers': total_speakers,
        'total_events': total_events,
        'total_tickets': total_tickets,
        'total_male': total_male,
        'total_female': total_female,
        'total_others': total_other,
        'upcoming_events': upcoming_events,
        'page': 'home',
    })

def schedules(request):
    all_events = Event.objects.all().filter(date__gte=timezone.now())
    total_results = all_events.count()
    page = request.GET.get('page', 1)
    results_per_page = 6
    paginator = Paginator(all_events, results_per_page)
    page_events = paginator.page(page)
    page_numbers = paginator.get_elided_page_range(page, on_each_side=2, on_ends=3)
    start_index = (page_events.number - 1) * results_per_page + 1
    end_index = min(start_index + results_per_page - 1, total_results)
    return render(request, 'schedules.html', {
        'events': page_events,
        'page_numbers': page_numbers,
        'start_index': start_index,
        'end_index': end_index,
        'page': 'schedules',
    })

def speakers(request):
    return render(request, 'speakers.html', {
        'page': 'speakers'
    })

def attendants(request):
    return render(request, 'attendants.html', {
        'page': 'attendants',
    })

def events(request):
    query = request.GET.get("query", "")
    all_events = Event.objects.all().order_by('-date')
    if query:
        all_events = all_events.filter(Q(title__icontains=query)|Q(details__icontains=query))
    total_results = all_events.count()
    page = request.GET.get('page', 1)
    results_per_page = 5
    paginator = Paginator(all_events, results_per_page)
    page_events = paginator.page(page)
    page_numbers = paginator.get_elided_page_range(page, on_each_side=2, on_ends=3)
    start_index = (page_events.number - 1) * results_per_page + 1
    end_index = min(start_index + results_per_page - 1, total_results)
    return render(request, 'events.html', {
        'events': page_events,
        'page_numbers': page_numbers,
        'start_index': start_index,
        'end_index': end_index,
        'query': query,
        'page': 'events',
    })

def event(request, slug=None):
    slug_event = Event.objects.get(slug=slug)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        total_price = slug_event.ticket_price * quantity
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('users:execute_payment')),
                "cancel_url": request.build_absolute_uri(reverse('users:payment_failed')),
            },
            "transactions": [
                {
                    "amount": {
                        "currency": "USD",
                        "total": 10,
                        "item_name": "SAMPLE",
                    },
                    "description": f"Payment for Ticket Booking (x{quantity})",
                }
            ],
        })

        if payment.create():
            return redirect(payment.links[1].href)  # Redirect to PayPal for payment
        else:
            return render(request, 'payment-failed.html')

    return render(request, 'event.html', {
        'event': slug_event,
        'page': 'events',
    })
    
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def payment_failed(request):
    return render(request, 'payment-failed.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment-success.html')
    else:
        return render(request, 'payment-failed.html')

def payment_checkout(request):
    return render(request, 'checkout.html')
       
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            if event.total_seats < 10 or event.total_seats > 1000:
                messages.error(request, "Please enter valid range for the seats (between 10 and 1000)")  
            else:    
                event.save()        
                messages.success(request, "The event was successfuly created")
                return redirect('users:events')
        else:
            messages.error(request, "Error creating event. Kindly fix the highlighted errors and try again")
    return render(request, 'create-event.html', {
        'form': form,
        'page': 'events',
    })
    
def update_event(request, slug):
    event = Event.objects.get(slug=slug)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            if event.total_seats < 10 or event.total_seats > 1000:
                messages.error(request, "Please enter valid range for the seats (between 10 and 1000)")  
            else:    
                event.save()        
                messages.success(request, "The event was successfuly updated")
                return redirect('users:events')
        else:
            messages.error(request, "Error creating event. Kindly fix the highlighted errors and try again")
    return render(request, 'update-event.html', {
        'form': form,
        'event': event,
        'page': 'events',
    })

def delete_event(request, slug=None):
    slug_event = Event.objects.get(slug=slug)
    name = slug_event.title
    slug_event.delete()
    messages.error(request, f"The event {name} has been deleted successfully.")
    return redirect('users:events')

def calendar(request):
    return render(request, 'calendar.html', {
        'page': 'calendar',
    })

# venues
def venues(request):
    query = request.GET.get("query", "")
    all_venues = Venue.objects.all().order_by('-created_at')
    if query:
        all_venues = all_venues.filter(Q(title__icontains=query)|Q(details__icontains=query))
    total_results = all_venues.count()
    page = request.GET.get('page', 1)
    results_per_page = 5
    paginator = Paginator(all_venues, results_per_page)
    page_venues = paginator.page(page)
    page_numbers = paginator.get_elided_page_range(page, on_each_side=2, on_ends=3)
    start_index = (page_venues.number - 1) * results_per_page + 1
    end_index = min(start_index + results_per_page - 1, total_results)
    return render(request, 'venues.html', {
        'venues': page_venues,
        'page_numbers': page_numbers,
        'start_index': start_index,
        'end_index': end_index,
        'query': query,
        'page': 'venues',
    })

def venue(request, slug=None):
    slug_event = Venue.objects.get(slug=slug)
    return render(request, 'event.html', {
        'venue': slug_event,
        'page': 'venue',
    })
    
def create_venue(request):
    form = VenueForm()
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()   
            messages.success(request, "The venue was successfuly created")
            return redirect('users:venues')
        else:
            messages.error(request, "Error creating venue. Kindly fix the highlighted errors and try again")
    return render(request, 'create-venue.html', {
        'form': form,
        'page': 'events',
    })
    
def update_venue(request, slug):
    venue = Venue.objects.get(slug=slug)
    form = VenueForm(instance=venue)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, "The venue was successfuly updated")
            return redirect('users:venues')
        else:
            messages.error(request, "Error creating venue. Kindly fix the highlighted errors and try again")
    return render(request, 'update-venue.html', {
        'form': form,
        'venue': venue,
        'page': 'venues',
    })
    
def delete_venue(request, slug=None):
    slug_venue = Venue.objects.get(slug=slug)
    name = slug_venue.title
    slug_venue.delete()
    messages.error(request, f"The venue {name} has been deleted successfully.")
    return redirect('users:venues')

# speakers
def speakers(request):
    query = request.GET.get("query", "")
    all_speakers = Speaker.objects.all().order_by('-created_at')
    total_results = all_speakers.count()
    page = request.GET.get('page', 1)
    results_per_page = 5
    paginator = Paginator(all_speakers, results_per_page)
    page_speakers = paginator.page(page)
    page_numbers = paginator.get_elided_page_range(page, on_each_side=2, on_ends=3)
    start_index = (page_speakers.number - 1) * results_per_page + 1
    end_index = min(start_index + results_per_page - 1, total_results)
    return render(request, 'speakers.html', {
        'speakers': page_speakers,
        'page_numbers': page_numbers,
        'start_index': start_index,
        'end_index': end_index,
        'query': query,
        'page': 'speakers',
    })

    
def create_speaker(request):
    form = SpeakerForm()
    if request.method == 'POST':
        form = SpeakerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()   
            messages.success(request, "The speaker was successfuly created")
            return redirect('users:speakers')
        else:
            messages.error(request, "Error creating speaker. Kindly fix the highlighted errors and try again")
    return render(request, 'create-speaker.html', {
        'form': form,
        'page': 'events',
    })
    
def update_speaker(request, slug):
    speaker = Speaker.objects.get(slug=slug)
    form = SpeakerForm(instance=speaker)
    if request.method == 'POST':
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, "The speaker was successfuly updated")
            return redirect('users:speakers')
        else:
            messages.error(request, "Error creating speaker. Kindly fix the highlighted errors and try again")
    return render(request, 'update-speaker.html', {
        'form': form,
        'speaker': speaker,
        'page': 'speakers',
    })
    
def delete_speaker(request, slug=None):
    slug_speaker = Speaker.objects.get(slug=slug)
    name = slug_speaker.title
    slug_speaker.delete()
    messages.error(request, f"The speaker {name} has been deleted successfully.")
    return redirect('users:speakers')