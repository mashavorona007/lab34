from functools import partial

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import View

from django.db import transaction
from django.http import HttpResponseBadRequest

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from users.forms import SettingsForm


class LoginPage(View): 
    template_name = 'users/login.html'
    
    class Failure: 
        LOGIN_FAILED = 0
        ACCOUNT_DISABLED = 1
    
    def get(self, request): 
        getData = request.GET
        cookies = request.COOKIES
        
        context = {}
        
        if 'LOGIN_FAILURE' in cookies:
            try: 
                failure = int(cookies['LOGIN_FAILURE'])
            except ValueError: 
                failure = None
            try: 
                context['errMsg'] = {
                    self.Failure.LOGIN_FAILED: "Authentication unsuccessful.", 
                    self.Failure.ACCOUNT_DISABLED: "Your account has been disabled. If this is unexpected, please contact the site administrator for help."
                }[failure]
                
            except KeyError: 
                pass # Silently fail
                
        response = render(request, self.template_name, context)
        response.delete_cookie('LOGIN_FAILURE')
        
        return response
    
    def return_failure(self, request, failure): 
        response = redirect(request.get_full_path())
        response.set_cookie('LOGIN_FAILURE', failure)
        return response
    
    def post(self, request): 
        login_failure = partial(
            self.return_failure, 
            request)
            
        postData = request.POST
        
        try: 
            username = postData['username']
            password = postData['password']
        except KeyError: 
            return HttpResponseBadRequest("Something went wrong.")
        
        userQuery = User.objects.filter(username__iexact=username)
        
        if userQuery.exists(): 
            assert userQuery.count() == 1
            username = userQuery[0].username
        
        user = authenticate(username=username, password=password)
        
        if user is not None: 
            if user.is_active: 
                login(request, user)
                
                # Everything is okay
                return redirect('index')
                
            else: 
                return login_failure(self.Failure.ACCOUNT_DISABLED)
                
        else: 
            return login_failure(self.Failure.LOGIN_FAILED)
            
    
class RegisterPage(View): 
    template_name = 'users/register.html'
    
    class Failure: 
        USERNAME_TAKEN = 0
        PASSWORD_MISMATCH = 1
        
    def get(self, request): 
        getData = request.GET
        cookies = request.COOKIES
        
        context = {}
        
        if 'REGISTER_FAILURE' in cookies:
            try: 
                failure = int(cookies['REGISTER_FAILURE'])
            except ValueError: 
                failure = None
            try: 
                context['errMsg'] = {
                    self.Failure.USERNAME_TAKEN: "We're sorry, but that username is taken. Please try a different username.", 
                    self.Failure.PASSWORD_MISMATCH: "Oh no! The two passwords you entered did not match!"
                }[failure]
                
            except KeyError: 
                pass # Silently fail
                
        response = render(request, self.template_name, context)
        response.delete_cookie('LOGIN_FAILURE')
        
        return response
        
    def return_failure(self, request, failure): 
        response = redirect(request.get_full_path())
        response.set_cookie('REGISTER_FAILURE', failure)
        return response
        
    def post(self, request): 
        register_failure = partial(
            self.return_failure, request)
            
        postData = request.POST
        
        try: 
            username = postData['username']
            email = postData['email']
            password1 = postData['password1']
            password2 = postData['password2']
        except KeyError: 
            return HttpResponseBadRequest("Bad Request!")
        
        if not username or not password1: 
            return HttpResponseBadRequest("Bad Request!")
            
        if User.objects.filter(username__iexact=username).exists(): 
            return register_failure(self.Failure.USERNAME_TAKEN)
            
        if password1 != password2: 
            return register_failure(self.Failure.PASSWORD_MISMATCH)
            
        newUser = User.objects.create_user(
            username=username, 
            email=email, 
            password=password1,
        )
        newUser.save()
        
        user = authenticate(username=username, password=password1)
        login(request, user)
        
        return redirect('index')
    
class LogoutPage(View): 
    template_name = 'users/logout.html'
    
    def get(self, request): 
        logout(request)
        return redirect('logout_landing')
        
class LogoutLandingPage(View): 
    template_name = 'users/logout.html'
    
    def get(self, request): 
        cookies = request.COOKIES
        
        if 'LOGOUT_LANDING' not in cookies: 
            return redirect('index')
            
        return render(request, self.template_name, {})
        
        
class SettingsPage(View):
    template_name = 'users/settings.html'
    
    @method_decorator(login_required)
    def dispatch(self, request):
        return super(SettingsPage, self).dispatch(request)
        
    def get(self, request):
        user = request.user
        
        context = {
            'settingsForm'  :   SettingsForm(initial={'email' : user.email}),
        }
        
        return render(request, self.template_name, context)
        
    def post(self, request):
        postData = request.POST
        
        user = request.user
        
        settingsForm = SettingsForm(postData)
        settingsForm.user = user
        
        if settingsForm.is_valid():
            cleanedData = settingsForm.cleaned_data
            
            email = cleanedData['email']
            password = cleanedData['password']
            newPassword1 = cleanedData['new_password1']
            newPassword2 = cleanedData['new_password2']
            
            with transaction.atomic():
                if password or newPassword1 or newPassword2:
                    user.set_password(newPassword1)
                    user.save()
                    
                    user = authenticate(
                        username=user.username,
                        password=newPassword1,
                    )
                    
                    assert user is not None
                    
                    login(request, user)
                    
                user.email = email
                user.save()
                
            messages.add_message(
                request,
                messages.SUCCESS,
                "Success! Profile updated.",
            )
            
            return redirect(request.get_full_path())
            
        else:
            context = {
                'settingsForm'  :   settingsForm,
            }
            
            return render(request, self.template_name, context)
            
            