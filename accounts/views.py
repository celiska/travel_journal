from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile


# Create your views here.
class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    # Login user automatically after signup
    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

@login_required
def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'registration/update.html', {'user_form': user_form, 'profile_form': profile_form})

def profile_view(request, username):
    user_account = User.objects.get(username=username)
    profile = Profile.objects.get(user__username=username)
    return render(request, 'registration/profile.html', {'user_account': user_account, 'profile': profile})
