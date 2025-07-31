from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Contact
from .forms import ContactForm

# Create your views here.

def health_check(request):
    """Simple health check endpoint"""
    return HttpResponse("OK", content_type="text/plain")

def contact_list(request):
    """Display all contacts"""
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

def contact_detail(request, pk):
    """Display a specific contact"""
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'contacts/contact_detail.html', {'contact': contact})

def contact_create(request):
    """Create a new contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Add New Contact'})

def contact_update(request, pk):
    """Update an existing contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Edit Contact'})

def contact_delete(request, pk):
    """Delete a contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})

# API views for AJAX calls
@csrf_exempt
@require_http_methods(["GET"])
def api_contact_list(request):
    """API endpoint to get all contacts as JSON"""
    contacts = Contact.objects.all()
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
    """API endpoint to create a new contact"""
    try:
        data = json.loads(request.body)
        contact = Contact.objects.create(
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
    """API endpoint to update a contact"""
    try:
        contact = get_object_or_404(Contact, pk=pk)
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
    """API endpoint to delete a contact"""
    try:
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
