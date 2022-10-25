from os import O_TEMPORARY
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Lead
from .forms import LeadModelForm,CustomUserCreationForm


class SignUpView(generic.CreateView):
    template_name="registration/signup.html"
    form_class= CustomUserCreationForm
    def get_success_url(self):
        return reverse("login")

class LeadListView(generic.ListView):
    template_name="leads/lead_list.html"
    queryset=Lead.objects.all()
    context_object_name="leads"

def lead_list(request):
    leads = Lead.objects.all()
    #return HttpResponse("Hello World")
    context={
        "leads":leads
    }
    return render(request , "leads/lead_list.html",context)

class LeadDetailView(generic.DetailView):
    template_name="leads/lead_detail.html"
    queryset=Lead.objects.all()
    context_object_name="Lead"

def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context={
        "Lead":lead
    }
    return render(request,"leads/lead_detail.html",context)

class LeadCreateView(generic.CreateView):
    template_name="leads/lead_create.html"
    form_class= LeadModelForm
    #queryset=Lead.objects.all()
    context_object_name="form"
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        body="Name : " + form.data['first_name'] +" "+ form.data['last_name']
        # for i in body:
        print(body)
        send_mail(
            'New Lead Added',
            body,
            'djangocrmadarsh@gmail.com',
            ['adarshbolettin1997@gmail.com'],
            fail_silently=False,
        )
        return super(LeadCreateView,self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if(request.method=="POST"):
        form = LeadModelForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("/leads")
    context={
        "form": form
    }
    return render(request, "leads/lead_create.html",context)


class LeadUpdateView(generic.UpdateView):
    template_name="leads/lead_update.html"
    queryset=Lead.objects.all()
    form_class=LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if(request.method=="POST"):
        form = LeadModelForm(request.POST,instance=lead)
        if(form.is_valid):
            form.save()
            return redirect("/leads")
    context={
        "lead":lead,
        "form":form
    }
    return render(request,"leads/lead_update.html",context)

class LeadDeleteView(generic.DeleteView):
    template_name="leads/lead_delete.html"
    queryset=Lead.objects.all()
    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request,pk):
    if(request.method=="POST"):
        lead=Lead.objects.get(id=pk)
        lead.delete()
        return redirect("/leads")
    return render(request,"leads/lead_delete.html")