from django.contrib import admin
from .models import *

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):          
    list_display = ('name', 'email', 'gender', 'created_at',)
    search_fields = ('name', 'email',)
    list_filter = ('gender',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'venue', 'created_at',)
    search_fields = ('title', 'venue',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at',)
    search_fields = ('event', 'user',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'created_at',)
    search_fields = ('name', 'location',)

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'created_at',)
    search_fields = ('name', 'details',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'deadline', 'location',)
    search_fields = ('title', 'location', 'company,')

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at',)
    search_fields = ('name', 'email',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'speaker', 'created_at',)
    search_fields = ('title', 'speaker',)

@admin.register(Attendant)
class AttendantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at',)
    search_fields = ('user', 'event',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'details')
    search_fields = ('user', 'event', 'details',)

@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum', 'details')
    search_fields = ('user', 'forum', 'details',)