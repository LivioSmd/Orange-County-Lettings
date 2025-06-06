from django.shortcuts import render
from profiles.models import Profile


def index(request):
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
