import datetime

from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import is_visit_long
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        entered_at = localtime(visit.entered_at)
        duration = get_duration(visit)
        is_strange = is_visit_long(visit, minutes=60)
        non_closed_visits.append(
            {
                'who_entered': visit.passcard,
                'entered_at': entered_at,
                'duration': format_duration(duration),
                'is_strange': is_strange
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
