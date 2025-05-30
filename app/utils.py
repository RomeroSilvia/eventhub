
from django.shortcuts import render
from django.utils import timezone


def countdown_timer(target_time):
    if target_time:
        if not getattr(target_time, 'tzinfo', None):
            target_time = timezone.make_aware(target_time)
        time_remaining = target_time - timezone.now()
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
   
        if days<0 or hours<0 or minutes<0 and seconds<=0:
            return {
                'days': 0,
                'completed': True,
                'hours': 0,
                'minutes': 0,
                'seconds': 0
            }
        else:
            return {
                        'days': days,
                        'completed': False,
                        'hours': hours,
                        'minutes': minutes,
                        'seconds': seconds
                    }
        
    