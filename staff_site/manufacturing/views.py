from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import LockMessage
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from backendIntegrations.models import LockPurchaseRequests

# Create your views here.


@login_required
def main(request):
	return render(request, 'manufacturing/home.html')


@login_required
def lock_incoming(request):
	context = {
		'incoming_messages': LockPurchaseRequests.objects.using('lr_backend_main').all()
	}
	return render(request, 'manufacturing/incoming_list.html', context)


@login_required
def approve_request(request, pk):
	incoming_request = LockPurchaseRequests.objects.using('lr_backend_main').get(
		pk=pk
	)
	incoming_request.status = 'OK'
	incoming_request.save()
	context = {
		'incoming_message': incoming_request
	}
	return HttpResponseRedirect(reverse('sales-detail', args=(pk,)))


@login_required
def decline_request(request, pk):
	incoming_request = LockPurchaseRequests.objects.using('lr_backend_main').get(
		pk=pk
	)
	incoming_request.status = 'FAIL'
	incoming_request.save()
	context = {
		'incoming_message': incoming_request
	}
	return HttpResponseRedirect(reverse('sales-detail', args=(pk,)))


@login_required
class PostListView(ListView):
	model = LockPurchaseRequests
	template_name = 'sales/incoming_list.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'incoming_messages'
	ordering = ['-created_at']


@method_decorator(login_required, name='dispatch')
class IncomingDetailView(DetailView):
	model = LockPurchaseRequests
	context_object_name = 'incoming_message'
	template_name = 'sales/incoming_detail.html'

