from django.contrib import admin

from .models import User, Event, Checkpoint, Reward

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Checkpoint)
admin.site.register(Reward)
