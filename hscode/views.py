from django.shortcuts import render, redirect
from django.views.generic import View
from marketing.models import Signup
from django.contrib import messages


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'uni/index.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            Signup.objects.get(email=email)
            messages.info(request, "You're already subcribed, thanks though.")
            return redirect('home')
        except Signup.DoesNotExist:
            new_signup = Signup()
            new_signup.email = email
            new_signup.save()
            messages.success(
                request, "Thank you for your subscription, now you'll be charge 15$ a month...")
            return redirect('home')


def profile(request):
    context = {
        'title': request.user
    }
    return render(request, "uni/profile.html", context)
