from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
# from .models import LockMessage
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.views.generic.edit import FormMixin, FormView

from backendIntegrations.models import LockPurchaseRequests, RegisterLock
from .filters import RequestFilter
from .forms import LockPurchaseForm
# Create your views here.

User = get_user_model()


@login_required
def main(request):
	return render(request, 'sales/home.html')


@login_required
def lock_incoming(request):
	context = {
		'incoming_messages': LockPurchaseRequests.objects.using('lr_backend_main').all()
	}
	return render(request, 'sales/incoming_list.html', context)


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


@method_decorator(login_required, name='dispatch')
class IncomingListView(ListView):
	model = LockPurchaseRequests
	template_name = 'sales/incoming_list.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'incoming_messages'
	ordering = ['-created_at']

	def get_context_data(self, **kwargs):
		context = super(IncomingListView, self).get_context_data(**kwargs)
		lock_filtered_list = RequestFilter(self.request.GET, queryset=self.queryset)
		context['filter'] = lock_filtered_list
		return context


@method_decorator(login_required, name='dispatch')
class IncomingDetailView(FormMixin, DetailView):
	model = LockPurchaseRequests
	form_class = LockPurchaseForm
	context_object_name = 'incoming_message'
	template_name = 'sales/sales_incoming_detail.html'

	def get_context_data(self, **kwargs):
		context = super(IncomingDetailView, self).get_context_data(**kwargs)
		form_final = LockPurchaseForm(
			initial={
				'status': self.object.status,
				'preferred_type': self.object.preferred_type,
				'internal_comment': self.object.internal_comment,
				'internal_status': self.object.internal_status,
				'quantity': self.object.quantity,
				"phone": self.object.phone,
				"company": self.object.company,
				"fio": self.object.fio,
				"email": self.object.email

			})
		context['lock_message_form'] = form_final
		context['incoming_message'] = self.get_object()
		try:
			employee = User.objects.get(pk=self.object.employee_id_sales)
			context['employee_email'] = employee.email
			context['employee_name'] = employee.full_name
		except Exception as e:
			context['employee_email'] = ""
			context['employee_name'] = ""

		return context

	def get_success_url(self):
		return reverse_lazy('sales-detail', kwargs={'pk': self.object.pk})

	def get_object(self):
		try:
			my_object = LockPurchaseRequests.objects.get(id=self.kwargs.get('pk'))
			return my_object
		except self.model.DoesNotExist:
			raise Http404("No MyModel matches the given query.")

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			self.object.status = form.cleaned_data["status"]
			self.object.preferred_type = form.cleaned_data["preferred_type"]
			self.object.internal_comment = form.cleaned_data["internal_comment"]
			self.object.internal_status = form.cleaned_data["internal_status"]
			self.object.quantity = form.cleaned_data["quantity"]
			if form.cleaned_data["phone"]:
				self.object.phone = form.cleaned_data["phone"]
			if form.cleaned_data["email"]:
				self.object.email = form.cleaned_data["email"]
			if form.cleaned_data["fio"]:
				self.object.fio = form.cleaned_data["fio"]
			if form.cleaned_data["company"]:
				self.object.company = form.cleaned_data["company"]
			self.object.employee_id_sales = self.request.user.id
			self.object.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		# put logic here
		return super(IncomingDetailView, self).form_valid(form)

	def form_invalid(self, form):
		# put logic here
		return super(IncomingDetailView, self).form_invalid(form)


class SalesDeleteView(LoginRequiredMixin, DeleteView):
	model = LockPurchaseRequests
	template_name = 'sales/confirm_delete.html'
	success_url = '/sales/inbox/'


@login_required
def get_lock_count(request):
	print("OK")
	if request.is_ajax and request.method == "GET":
		type_lock = request.GET.get('type')
		count = RegisterLock.objects.all().filter(
			current_type=2,
			current_stage=4,
			version=type_lock
		).count()
		# send to client side.

		return JsonResponse({"count": count}, status=200)

	# some error occured
	return JsonResponse({"error": ""}, status=400)