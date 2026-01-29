# SmartCity Insight - Complete HTML Template Package

## 📋 Overview

This package contains a complete set of responsive HTML pages for **SmartCity Insight**, a web application for urban issue management aligned with SDG 11 (Sustainable Cities and Communities).

## 🎨 Design Philosophy

The interface features a **civic/government aesthetic** with:
- Professional, trustworthy appearance
- Clear hierarchy and accountability indicators
- Accessible, readable typography (Bitter serif + Work Sans sans-serif)
- Civic color palette (forest green primary, amber secondary)
- Transparent data visualization
- Mobile-first responsive design

## 📁 File Structure

### Core Pages

1. **index.html** - Public Home Page (Before Login)
   - Application introduction
   - SDG 11 alignment messaging
   - Login/Register call-to-action
   - NO complaint data or registration button visible

2. **register.html** - User Registration Page
   - Complete signup form with all required fields
   - Locality/ward selection
   - Form validation ready

3. **login.html** - User Login Page
   - Email and password authentication
   - Role auto-detection note
   - Password recovery option

4. **dashboard.html** - Authenticated Home Page (Locality Dashboard)
   - Locality-level statistics (total, resolved, pending)
   - Pie chart visualization (Chart.js)
   - Conditional rendering with Django templates
   - "Register Complaint" button (only when logged in)
   - Recent activity feed

5. **register-complaint.html** - Complaint Registration Form
   - Issue type dropdown (Garbage/Pothole/Streetlight)
   - Interactive map (Leaflet.js) for location selection
   - Image upload with preview
   - Character counter for description
   - Auto-timestamp and status notes

6. **complaints.html** - Complaint Listing Page
   - Locality-wise complaint display
   - Advanced filtering (status, type, SLA)
   - Card-based layout with before/after images
   - SLA status indicators
   - Pagination support

7. **profile.html** - User Profile Page
   - User-specific complaint history
   - Personal statistics
   - Toggle between card and table view
   - Account details display

8. **admin-dashboard.html** - Ward Admin Dashboard
   - Restricted to Admin users only
   - SLA breach alerts
   - Interactive complaint map
   - Bulk complaint management
   - Resolution modal with image upload
   - Priority complaint sections

### Components

9. **navbar.html** - Reusable Navigation Component
   - Conditional rendering for auth state
   - User dropdown menu
   - Admin panel link (for admins only)
   - Mobile responsive hamburger menu

10. **styles.css** - Complete Stylesheet
    - CSS custom properties for theming
    - Responsive grid layouts
    - Component-based styling
    - Print-friendly styles
    - Animations and transitions

## 🔧 Technical Features

### Django Template Integration

All pages use Django-style template tags:

```django
{% if user.is_authenticated %}
  <!-- Authenticated content -->
{% else %}
  <!-- Public content -->
{% endif %}

{% for complaint in complaints %}
  <!-- Loop content -->
{% endfor %}

{% csrf_token %}
```

### Conditional Rendering Examples

**Dashboard Page:**
```django
{% if user.is_authenticated %}
  <div class="dashboard-main">
    <!-- Stats, charts, actions -->
  </div>
{% else %}
  <div class="auth-required">
    <!-- Login prompt -->
  </div>
{% endif %}
```

**Admin Dashboard:**
```django
{% if user.is_authenticated and user.role == 'Admin' %}
  <!-- Admin tools -->
{% else %}
  <div class="access-denied">
    <!-- Access restriction message -->
  </div>
{% endif %}
```

### External Libraries Used

1. **Google Fonts**
   - Bitter (serif, display)
   - Work Sans (sans-serif, body)

2. **Chart.js** (Dashboard)
   - Pie/doughnut chart for status distribution
   - CDN: `https://cdn.jsdelivr.net/npm/chart.js`

3. **Leaflet.js** (Maps)
   - Interactive location selection
   - Complaint mapping
   - CDN: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`

### Key CSS Custom Properties

```css
:root {
  --primary-color: #1e5a3f;     /* Forest green */
  --secondary-color: #d97706;    /* Amber */
  --success-color: #2a9d4e;      /* Green */
  --warning-color: #f59e0b;      /* Orange */
  --danger-color: #dc2626;       /* Red */
  --font-display: 'Bitter', serif;
  --font-body: 'Work Sans', sans-serif;
}
```

## 🔗 Django Backend Integration

### Required URL Patterns

```python
# urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-complaint/', views.register_complaint, name='register_complaint'),
    path('complaints/', views.complaints_list, name='complaints'),
    path('profile/', views.profile, name='profile'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('resolve-complaint/', views.resolve_complaint, name='resolve_complaint'),
]
```

### Required Context Variables

**Dashboard:**
```python
context = {
    'user': request.user,
    'total_complaints': int,
    'resolved_complaints': int,
    'pending_complaints': int,
    'sla_breached': int,
    'avg_resolution_time': str,
    'active_reporters': int,
    'recent_activities': QuerySet,
}
```

**Complaints List:**
```python
context = {
    'complaints': QuerySet,  # Paginated
    # Each complaint object should have:
    # - id, issue_type, description, status
    # - created_at, resolved_at, landmark
    # - before_image, after_image
    # - sla_status, days_pending
    # - user.name
}
```

**Admin Dashboard:**
```python
context = {
    'total_complaints': int,
    'pending_complaints': int,
    'resolved_complaints': int,
    'sla_breached_count': int,
    'resolution_rate': float,
    'sla_breached_complaints': QuerySet,
    'pending_complaints_list': QuerySet,
    'complaints_json': str,  # JSON for map markers
    'ward_center_lat': float,
    'ward_center_lng': float,
}
```

### Form Handling

**Registration:**
```python
# Expected POST data
{
    'name': str,
    'email': str,
    'password': str,
    'age': int,
    'mobile': str (10 digits),
    'locality': str,
}
```

**Complaint Registration:**
```python
# Expected POST data
{
    'issue_type': str,  # 'garbage', 'pothole', 'streetlight'
    'description': str,
    'latitude': float,
    'longitude': float,
    'landmark': str (optional),
    'before_image': File,
}
```

**Complaint Resolution (Admin):**
```python
# Expected POST data
{
    'complaint_id': int,
    'after_image': File,
    'resolution_notes': str (optional),
}
```

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

All layouts adapt gracefully across devices with:
- Flexible grid systems
- Collapsible navigation
- Touch-friendly controls
- Readable text at all sizes

## 🎯 SLA (Service Level Agreement) Implementation

The design includes SLA status indicators:

**Issue Types & Timelines:**
- Garbage: 24 hours
- Pothole: 72 hours
- Streetlight: 48 hours

**Status Colors:**
- Normal (green): Within SLA
- Breached (red): Exceeded SLA

Backend should calculate `days_pending` and set `sla_status` accordingly.

## 🔐 Access Control Logic

**Public Pages:**
- index.html (always accessible)
- login.html (always accessible)
- register.html (always accessible)

**Authenticated Pages:**
- dashboard.html (requires login)
- register-complaint.html (requires login)
- complaints.html (requires login)
- profile.html (requires login)

**Admin-Only Pages:**
- admin-dashboard.html (requires login + Admin role)

## 🎨 Customization Guide

### Changing Colors

Edit CSS custom properties in `styles.css`:

```css
:root {
  --primary-color: #YOUR_COLOR;
  --secondary-color: #YOUR_COLOR;
}
```

### Changing Fonts

Replace Google Fonts link in HTML `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

Update CSS:

```css
:root {
  --font-display: 'Your Font', serif;
  --font-body: 'Your Font', sans-serif;
}
```

### Adding New Status Types

Update badge styles in CSS:

```css
.status-badge.your-status {
    background-color: #color;
    color: #text-color;
}
```

## 📊 JavaScript Features

### Chart Initialization (Dashboard)

```javascript
// Automatic Chart.js pie chart
// Reads complaint data from Django context
// Customizable colors and animations
```

### Interactive Map (Complaint Registration)

```javascript
// Leaflet.js map
// Click to select location
// Updates hidden lat/lng inputs
// Marker placement
```

### File Upload Preview

```javascript
// Real-time image preview
// Before uploading to server
// Works for before_image and after_image
```

### Filtering System

```javascript
// Client-side filtering
// Instant results
// Multiple filter combinations
```

## 🚀 Deployment Checklist

- [ ] Set up Django backend with required views
- [ ] Configure media files for image uploads
- [ ] Set up database models for User and Complaint
- [ ] Implement authentication system
- [ ] Configure email for password reset
- [ ] Set up static files serving
- [ ] Test all forms and validations
- [ ] Configure map API keys if needed
- [ ] Set up proper CSRF protection
- [ ] Test responsive design on devices

## 📝 Notes for Developers

1. **Django Template Variables**: Replace placeholder values with actual backend data
2. **URL Names**: Ensure URL names match your Django urls.py configuration
3. **Media Files**: Configure MEDIA_ROOT and MEDIA_URL for image uploads
4. **Security**: Implement proper authentication checks in views
5. **Validation**: Add server-side validation for all forms
6. **SLA Calculation**: Implement background task to check SLA compliance
7. **Notifications**: Consider adding email/SMS notifications for status updates

## 🎯 Key Features Implemented

✅ Public home page without sensitive data  
✅ Complete user registration and login  
✅ Role-based access control (Citizen/Admin)  
✅ Locality-based complaint dashboard  
✅ Interactive map for location selection  
✅ Image upload with preview  
✅ SLA status indicators  
✅ Admin-only resolution workflow  
✅ Responsive design (mobile-first)  
✅ Professional government aesthetic  
✅ Accessibility considerations  
✅ Print-friendly layouts  

## 📧 Support

For questions or customization requests, refer to the inline comments in each file. All major sections are clearly commented for easy understanding and modification.

---

**Built for SDG 11: Sustainable Cities and Communities**  
*Making cities inclusive, safe, resilient and sustainable*
