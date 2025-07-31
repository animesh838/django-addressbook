from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import json
from .models import Contact
from .forms import ContactForm

def health_check(request):
    """Simple health check endpoint"""
    return HttpResponse("OK", content_type="text/plain")

def landing_page(request):
    """Landing page with login form"""
    if request.user.is_authenticated:
        return redirect('contacts:contact_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('contacts:contact_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'contacts/landing.html')

def register_page(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('contacts:contact_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'contacts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'contacts/register.html')
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f'Account created successfully! Welcome, {username}!')
        return redirect('contacts:contact_list')
    
    return render(request, 'contacts/register.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('contacts:landing_page')

@login_required
def contact_list(request):
    """Display all contacts for the logged-in user"""
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

@login_required
def contact_detail(request, pk):
    """Display a specific contact for the logged-in user"""
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    return render(request, 'contacts/contact_detail.html', {'contact': contact})

@login_required
def contact_create(request):
    """Create a new contact for the logged-in user"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Add New Contact'})

@login_required
def contact_update(request, pk):
    """Update a contact for the logged-in user"""
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Edit Contact'})

@login_required
def contact_delete(request, pk):
    """Delete a contact for the logged-in user"""
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('contacts:contact_list')
    
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})

# API views for AJAX calls
@csrf_exempt
@require_http_methods(["GET"])
def api_contact_list(request):
    """API endpoint to get all contacts for the logged-in user as JSON"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    contacts = Contact.objects.filter(user=request.user)
    data = []
    for contact in contacts:
        data.append({
            'id': contact.id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'email': contact.email,
            'phone': contact.phone,
            'address': contact.address,
            'city': contact.city,
            'state': contact.state,
            'zip_code': contact.zip_code,
            'country': contact.country,
            'notes': contact.notes,
            'created_at': contact.created_at.isoformat(),
            'updated_at': contact.updated_at.isoformat(),
        })
    return JsonResponse({'contacts': data})

@csrf_exempt
@require_http_methods(["POST"])
def api_contact_create(request):
    """API endpoint to create a new contact for the logged-in user"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        contact = Contact.objects.create(
            user=request.user,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            zip_code=data.get('zip_code', ''),
            country=data.get('country', ''),
            notes=data.get('notes', ''),
        )
        return JsonResponse({
            'success': True,
            'contact': {
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone': contact.phone,
                'address': contact.address,
                'city': contact.city,
                'state': contact.state,
                'zip_code': contact.zip_code,
                'country': contact.country,
                'notes': contact.notes,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def api_contact_update(request, pk):
    """API endpoint to update a contact for the logged-in user"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        contact = get_object_or_404(Contact, pk=pk, user=request.user)
        data = json.loads(request.body)
        
        contact.first_name = data.get('first_name', contact.first_name)
        contact.last_name = data.get('last_name', contact.last_name)
        contact.email = data.get('email', contact.email)
        contact.phone = data.get('phone', contact.phone)
        contact.address = data.get('address', contact.address)
        contact.city = data.get('city', contact.city)
        contact.state = data.get('state', contact.state)
        contact.zip_code = data.get('zip_code', contact.zip_code)
        contact.country = data.get('country', contact.country)
        contact.notes = data.get('notes', contact.notes)
        
        contact.save()
        
        return JsonResponse({
            'success': True,
            'contact': {
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone': contact.phone,
                'address': contact.address,
                'city': contact.city,
                'state': contact.state,
                'zip_code': contact.zip_code,
                'country': contact.country,
                'notes': contact.notes,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_contact_delete(request, pk):
    """API endpoint to delete a contact for the logged-in user"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        contact = get_object_or_404(Contact, pk=pk, user=request.user)
        contact.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def api_contact_detail(request):
    """API endpoint to search contacts by first name for the logged-in user"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    name = request.GET.get('name', '')
    
    if not name:
        return JsonResponse({'contacts': []})
    
    # Search for contacts with first_name containing the search term (case-insensitive)
    contacts = Contact.objects.filter(user=request.user, first_name__icontains=name)
    
    data = []
    for contact in contacts:
        data.append({
            'id': contact.id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'email': contact.email,
            'phone': contact.phone,
            'address': contact.address,
            'city': contact.city,
            'state': contact.state,
            'zip_code': contact.zip_code,
            'country': contact.country,
            'notes': contact.notes,
        })
    
    return JsonResponse({'contacts': data})
   