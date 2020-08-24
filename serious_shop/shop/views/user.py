from django.views.generic import View
from django.shortcuts import render


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, "profile.html")
