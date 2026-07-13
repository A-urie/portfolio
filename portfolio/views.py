import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Project
from .forms import ContactForm


def index(request):
    return render(request, 'portfolio/index.html')


def about(request):
    return render(request, 'portfolio/about.html')


def resume(request):
    return render(request, 'portfolio/resume.html')


def services(request):
    return render(request, 'portfolio/services.html')


def portfolio_list(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'portfolio/portfolio.html', context)


def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'project': project}
    return render(request, 'portfolio/portfolio_details.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"De : {name} <{email}>\n\n{message}"

            try:
                response = requests.post(
                    'https://api.brevo.com/v3/smtp/email',
                    headers={
                        'accept': 'application/json',
                        'api-key': os.environ.get('BREVO_API_KEY'),
                        'content-type': 'application/json',
                    },
                    json={
                        'sender': {'name': 'Portfolio Urie', 'email': 'angeuriebadou68@gmail.com'},
                        'to': [{'email': settings.CONTACT_EMAIL}],
                        'replyTo': {'email': email, 'name': name},
                        'subject': f"[Portfolio] {subject}",
                        'textContent': full_message,
                    },
                    timeout=10,
                )
                print("BREVO STATUS:", response.status_code)
                print("BREVO BODY:", response.text)
                response.raise_for_status()
                messages.success(request, "Votre message a bien été envoyé. Merci !")
            except requests.RequestException as e:
                print("BREVO ERROR:", str(e))
                messages.error(request, "Une erreur est survenue lors de l'envoi. Réessayez plus tard.")
            return redirect('portfolio:contact')
    else:
        form = ContactForm()

    return render(request, 'portfolio/contact.html', {'form': form})