from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    exceptional_abilities = forms.CharField(label='Exceptional Abilities')
    skills = forms.CharField(label='Skills')
    achievements = forms.CharField(label='Achievements')
    projects = forms.CharField(label='Projects')
    
    class Meta:
        model = UserProfile
        fields = ('exceptional_abilities', 'skills', 'achievements', 'projects')
        
    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile