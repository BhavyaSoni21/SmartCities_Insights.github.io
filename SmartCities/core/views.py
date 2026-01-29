from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Issue, UserProfile


def _attach_profile_attrs(request: HttpRequest) -> None:
    """
    Templates reference attributes like `user.name`, `user.role`, etc.
    Default Django `User` doesn't have these, so we attach them from UserProfile.
    """
    user = getattr(request, "user", None)
    if not user or not getattr(user, "is_authenticated", False):
        return

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "name": user.get_full_name() or user.get_username(),
            "role": "Citizen",
            "locality": "",
            "ward_number": "",
        },
    )

    # Monkeypatch common template fields onto `request.user`
    user.name = profile.name or user.get_full_name() or user.get_username()
    user.role = profile.role
    user.locality = profile.locality
    user.ward_number = profile.ward_number
    user.mobile = profile.mobile
    user.age = profile.age

def home(request: HttpRequest) -> HttpResponse:
    issues = Issue.objects.all()
    return render(request, 'home.html', {'issues': issues})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    # Placeholder context so templates render without crashing.
    _attach_profile_attrs(request)
    return render(
        request,
        'dashboard.html',
        {
            'total_complaints': 0,
            'resolved_complaints': 0,
            'pending_complaints': 0,
            'sla_breached': 0,
            'avg_resolution_time': '--',
            'active_reporters': 0,
            'recent_activities': [],
        },
    )


@login_required
def complaints(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    return render(request, 'complaints.html', {})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    return render(request, 'profile.html', {})


@login_required
def register_complaint(request: HttpRequest) -> HttpResponse:
    # Template expects a page; real saving can be added later.
    _attach_profile_attrs(request)
    if request.method == 'POST':
        messages.success(request, 'Complaint submitted (demo).')
        return redirect('complaints')
    return render(request, 'register-complaint.html', {})


@login_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    # Placeholder context to satisfy template variables.
    _attach_profile_attrs(request)
    return render(
        request,
        'admin-dashboard.html',
        {
            'sla_breached_count': 0,
            'total_complaints': 0,
            'monthly_complaints': 0,
            'pending_complaints': 0,
            'resolved_complaints': 0,
            'resolution_rate': 0,
            'sla_breached_complaints': [],
            'pending_complaints_list': [],
            'ward_center_lat': 19.0760,
            'ward_center_lng': 72.8777,
            'complaints_json': '[]',
        },
    )


@login_required
def resolve_complaint(request: HttpRequest) -> HttpResponse:
    # Endpoint referenced by admin-dashboard.html form.
    _attach_profile_attrs(request)
    if request.method != 'POST':
        return redirect('admin_dashboard')
    messages.success(request, 'Complaint marked as resolved (demo).')
    return redirect('admin_dashboard')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        # Temporary demo bypass: if demo credentials, auto-create account
        if email == 'demo@city.com' and password == 'demo12345':
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email, 'is_active': True}
                )
                if created:
                    user.set_password(password)
                    user.save()
                    # Create profile
                    UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': 'Demo User',
                            'role': 'Citizen',
                            'locality': 'Ward 1 - Central District',
                            'ward_number': '1',
                            'mobile': '9999999999',
                            'age': 25,
                        }
                    )
                elif not user.check_password(password):
                    user.set_password(password)
                    user.save()
                auth_login(request, user)
                _attach_profile_attrs(request)
                messages.success(request, 'Logged in successfully.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Database error. Please register a new account or check database permissions.')
                return render(request, 'login.html', {})

        # Normal authentication
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html', {})

        auth_login(request, user)
        _attach_profile_attrs(request)
        messages.success(request, 'Logged in successfully.')
        return redirect('dashboard')
    return render(request, 'login.html', {})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        from django.contrib.auth import get_user_model

        User = get_user_model()
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        name = (request.POST.get('name') or '').strip()
        mobile = (request.POST.get('mobile') or '').strip()
        age_raw = (request.POST.get('age') or '').strip()
        locality = (request.POST.get('locality') or '').strip()

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'register.html', {})

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists. Please log in.')
            return redirect('login')

        user = User.objects.create_user(username=email, email=email, password=password)
        profile = UserProfile.objects.create(
            user=user,
            name=name or email,
            role='Citizen',
            locality=locality,
            ward_number='',
            mobile=mobile,
            age=int(age_raw) if age_raw.isdigit() else None,
        )
        profile.save()

        messages.success(request, 'Account created. Please log in.')
        return redirect('login')
    return render(request, 'register.html', {})


def logout_view(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    # Navbar uses this named URL; always return to home.
    return redirect(reverse('home'))
