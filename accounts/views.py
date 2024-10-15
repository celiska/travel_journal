from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from viewer.models import Entry
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
    entries = Entry.objects.filter(author=user_account)
    return render(request, 'registration/profile.html', {'user_account': user_account, 'profile': profile, 'entries': entries})

@login_required
def delete_user(request):
    if request.method == 'POST':
        u = User.objects.get(username=request.user.username)
        logout(request)
        u.delete()
        return redirect('home')
    else:
        return render(request, 'registration/delete.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile', username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/password_change.html', {'form': form})

def profile_view(request, username):
    user_account = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_account)
    entries = Entry.objects.filter(author=user_account)

    is_editor_or_superuser = request.user.is_superuser or request.user.groups.filter(name='editor').exists()

    return render(request, 'registration/profile.html', {
        'user_account': user_account,
        'profile': profile,
        'entries': entries,
        'is_editor_or_superuser': is_editor_or_superuser,
    })