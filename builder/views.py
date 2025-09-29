from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Experience, Education
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

@login_required
def dashboard(request):
    # ✅ ensure profile exists and is saved
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # update profile
        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.summary = request.POST.get('summary')
        profile.skills = request.POST.get('skills')  # ✅ fixed
        profile.save()

        # clear old and save new experiences
        profile.experience_set.all().delete()
        companies = request.POST.getlist('company')
        positions = request.POST.getlist('position')
        start_dates_exp = request.POST.getlist('start_date_exp')
        end_dates_exp = request.POST.getlist('end_date_exp')
        descriptions = request.POST.getlist('description')

        for i in range(len(companies)):
            if companies[i].strip():  # avoid empty entries
                Experience.objects.create(
                    profile=profile,
                    company=companies[i],
                    position=positions[i],
                    start_date=start_dates_exp[i],
                    end_date=end_dates_exp[i] if end_dates_exp[i] else None,
                    description=descriptions[i]
                )

        # clear old and save new educations
        profile.education_set.all().delete()
        institutions = request.POST.getlist('institution')
        degrees = request.POST.getlist('degree')
        fields = request.POST.getlist('field_of_study')
        grad_dates = request.POST.getlist('graduation_date')

        for i in range(len(institutions)):
            if institutions[i].strip():  # avoid empty entries
                Education.objects.create(
                    profile=profile,
                    institution=institutions[i],
                    degree=degrees[i],
                    field_of_study=fields[i],
                    graduation_date=grad_dates[i]
                )

        return redirect('resume_view', profile_id=profile.id)  # ✅ fixed

    return render(request, 'dashboard.html', {'profile': profile})


def resume_view(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    # split skills string into a list
    profile.skills_list = [skill.strip() for skill in profile.skills.split(',')] if profile.skills else []
    return render(request, 'resume_template.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def download_resume(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.skills_list = [skill.strip() for skill in profile.skills.split(',')] if profile.skills else []

    template_path = 'resume_template_pdf.html'  # use a slightly different template for pdf
    context = {'profile': profile}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile.name}_resume.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
