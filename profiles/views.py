from django.shortcuts import render
from profiles.models import Profile


def index(request):
    """
    Display a list of all user profiles.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, profile_id):
    """
    Display details for a single user profile.
    """
    profile = Profile.objects.get(id=profile_id)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
