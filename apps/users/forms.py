from django import forms
from apps.users.models import Account, Event, Speaker, Venue, Comment, Ticket, Job, Forum, ForumComment
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(attrs={
            'type':'password',
            'placeholder': 'Enter password',
        }),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'type':'password',
            'placeholder': 'Confirm password',
        }),
    )

    class Meta:
        model = Account
        fields = ('email', 'name', 'password1', 'password2')
        widgets = {
            'name':forms.TextInput(attrs={
                'autofocus': '',
                'placeholder': 'Your name',
            }),
            'email':forms.EmailInput(attrs={
                'autofocus': 'off',
                'placeholder': 'Your email',
            }),

        }

class LoginForm(forms.ModelForm):
    class Meta:
        model  =  Account
        fields =  ('email', 'password')
        widgets = {
            'email':forms.EmailInput(attrs={
                'autofocus': '',
                'class':'mb-2',
                'placeholder': 'Your email',
            }),
            'password':forms.PasswordInput(attrs={
                'class':'mb-2',
                'placeholder': 'Your password',
            }),
        }

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

class EventForm(forms.ModelForm):
    class Meta:
        model  =  Event
        fields =  ('title', 'image', 'event_type', 'event_status', 'venue', 'date', 'time', 'speaker', 'total_seats', 'details', 'ticket_price')
        widgets = {
            'date':forms.DateInput(attrs={
                'type': 'date',
            }),
            'time':forms.TimeInput(attrs={
                'type': 'time',
            }),
            'ticket_price':forms.NumberInput(attrs={
                'step': '1',
            }),
            
        }
        
class TicketForm(forms.ModelForm):
    class Meta:
        model  =  Ticket
        fields =  ('event', 'quantity', )
        widgets = {
            'quantity':forms.NumberInput(attrs={
                'step': '1',
            }),
            
        }
        
class JobForm(forms.ModelForm):
    class Meta:
        model  =  Job
        fields =  ('title', 'company', 'deadline', 'location', 'details', 'attachment' )
        widgets = {
            'deadline':forms.DateInput(attrs={
                'type': 'date',
            }),            
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model  =  Venue
        fields =  ('name', 'location', 'capacity', 'image', 'details',)
        widgets = {
            'capacity':forms.NumberInput(attrs={
                'step': '1',
            }),
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model  =  Forum
        fields =  ('name', 'details', 'image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model  =  Comment
        fields =  ('rating', 'details')
        widgets = {
            'rating':forms.NumberInput(attrs={
                'step': '1',
                'min': '1',
                'max': 5,
            }),
        }

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model  =  ForumComment
        fields =  ( 'details',)

class SpeakerForm(forms.ModelForm):
    class Meta:
        model  =  Speaker
        fields =  ('name', 'email', 'bio', 'image', 'phone', 'career', 'gender')
    