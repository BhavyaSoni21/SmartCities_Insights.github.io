from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

LOCALITY_WARD_CHOICES = [
    ('', '-- Select Locality --'),
    ('Andheri|1', 'Andheri (Ward 1)'),
    ('Bandra|2', 'Bandra (Ward 2)'),
    ('Borivali|3', 'Borivali (Ward 3)'),
    ('Chembur|4', 'Chembur (Ward 4)'),
    ('Dadar|5', 'Dadar (Ward 5)'),
    ('Goregaon|6', 'Goregaon (Ward 6)'),
    ('Ghatkopar|7', 'Ghatkopar (Ward 7)'),
    ('Juhu|8', 'Juhu (Ward 8)'),
    ('Kandivali|9', 'Kandivali (Ward 9)'),
    ('Kurla|10', 'Kurla (Ward 10)'),
    ('Malad|11', 'Malad (Ward 11)'),
    ('Mulund|12', 'Mulund (Ward 12)'),
    ('Powai|13', 'Powai (Ward 13)'),
    ('Santacruz|14', 'Santacruz (Ward 14)'),
    ('Thane|15', 'Thane (Ward 15)'),
    ('Vikhroli|16', 'Vikhroli (Ward 16)'),
    ('Vile Parle|17', 'Vile Parle (Ward 17)'),
    ('Worli|18', 'Worli (Ward 18)'),
]

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        help_text='Email cannot be changed for security reasons'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    locality = forms.ChoiceField(
        choices=LOCALITY_WARD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select your residential area - ward will be assigned automatically'
    )
    
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile', 'locality', 'age']

