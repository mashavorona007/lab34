from __future__ import unicode_literals

from django import forms

from utils.decorators import html5_required


@html5_required
class SettingsForm(forms.Form):
    email = forms.EmailField()
    
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
    new_password1 = forms.CharField(
        label="New Password",
        required=False,
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        label="New Password (Again)",
        required=False,
        widget=forms.PasswordInput(),
    )
    
    user = None
    
    def clean(self):
        super(SettingsForm, self).clean()
        
        password = self.cleaned_data['password']
        newPassword1 = self.cleaned_data['new_password1']
        newPassword2 = self.cleaned_data['new_password2']
        
        if password or newPassword1 or newPassword2:
            assert self.user is not None
            
            # Incorrect password
            if not self.user.check_password(password):
                self.add_error('password', "Password incorrect!")
                
            # Empty new password
            if not newPassword1:
                self.add_error(
                    'new_password1',
                    "New password cannot be empty!",
                )
                
            # Passwords don't match
            if newPassword1 != newPassword2:
                self.add_error('new_password1', "Passwords don't match!")
                
                