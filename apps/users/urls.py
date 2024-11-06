from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedules/', views.schedules, name='schedules'),
    path('attendants/', views.attendants, name='attendants'),
    
    # events
    path('events/', views.events, name='events'),
    path('events/get/', views.get_events, name='get_events'),
    path('events/comment/<slug:slug>/', views.post_comment, name='post-comment'),
    path('events/create', views.create_event, name='create-event'),
    path('events/register', views.register_event, name='register-event'),
    path('events/update/<slug:slug>/', views.update_event, name='update-event'),
    path('events/delete/<slug:slug>/', views.delete_event, name='delete-event'),
    path('events/<slug:slug>/', views.event, name='event'),
    
    # venues
    path('venues/', views.venues, name='venues'),
    path('venues/create', views.create_venue, name='create-venue'),
    path('venues/update/<slug:slug>/', views.update_venue, name='update-venue'),
    path('venues/delete/<slug:slug>/', views.delete_venue, name='delete-venue'),
    path('venues/<slug:slug>/', views.venue, name='venue'),
    
    # venues
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/create', views.create_job, name='create-job'),
    
    # forums
    path('forums/', views.forums, name='forums'),
    path('forums/comment/<slug:slug>/', views.forum_comment, name='forum-comment'),
    path('forums/create', views.create_forum, name='create-forum'),
    path('forums/update/<slug:slug>/', views.update_forum, name='update-forum'),
    path('forums/delete/<slug:slug>/', views.delete_forum, name='delete-forum'),
    path('forums/<slug:slug>/', views.forum, name='forum'),
    
    # speakers
    path('speakers/', views.speakers, name='speakers'),
    path('speakers/create', views.create_speaker, name='create-speaker'),
    path('speakers/update/<slug:slug>/', views.update_speaker, name='update-speaker'),
    path('speakers/delete/<slug:slug>/', views.delete_speaker, name='delete-speaker'),
    
    path('calendar/', views.calendar, name='calendar'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_user, name='logout'),
    
    # checkout
    path('checkout/', views.payment_checkout, name='checkout_payment'),
    # path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('execute_payment/failed', views.payment_failed, name='payment_failed'),
]