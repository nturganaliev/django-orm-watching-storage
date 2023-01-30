import datetime

from django.contrib import messages
from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import is_visit_long
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = passcard.visit_set.all()
    this_passcard_visits = []

    for visit in visits:
        if visit.leaved_at is not None:
            entered_at = localtime(visit.entered_at)
            duration = get_duration(visit)
            is_strange = is_visit_long(visit, minutes=60)
            this_passcard_visits.append({
                'entered_at': entered_at,
                'duration': format_duration(duration),
                'is_strange': is_strange
            })
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
