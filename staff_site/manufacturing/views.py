import datetime
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from .models import LockMessage
from django.urls import reverse
from django.utils.decorators import method_decorator

from .pdf_generator import PdfGenerator
from .filters import LockFilter

from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from backendIntegrations.models import LockPurchaseRequests, RegisterLock, RegisterKey, LockWithManuals, LockGeneratedUserFiles
from .forms import LockCreateForm, LockUpdateManufacturingForm, MasterKeyUpdateManufacturingForm


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


@method_decorator(login_required, name='dispatch')
class LockRequestsManufacturingListView(ListView):
	model = LockPurchaseRequests
	template_name = 'manufacturing/incoming_list.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'incoming_messages'
	ordering = ['-created_at']


@method_decorator(login_required, name='dispatch')
class LockListView(ListView):

	model = RegisterLock
	template_name = 'manufacturing/lock_list.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'locks'
	ordering = ['-created_at']

	def get_context_data(self, **kwargs):
		context = super(LockListView, self).get_context_data(**kwargs)
		lock_filtered_list = LockFilter(self.request.GET, queryset=self.queryset)
		context['filter'] = lock_filtered_list
		return context


@method_decorator(login_required, name='dispatch')
class LockDetailView(DetailView):
	model = RegisterLock
	context_object_name = 'lock'

	template_name = 'manufacturing/lock_detail.html'

	def get_context_data(self, **kwargs):
		context = super(LockDetailView, self).get_context_data(**kwargs)
		try:
			manual = LockWithManuals.objects.get(lock_id=self.kwargs['pk'])
			context['manual_url'] = manual.manual.file.url
		except Exception as e:
			context['manual_url'] = "#"
		try:
			user_file = LockGeneratedUserFiles.objects.using('lr_backend_main').all().filter(
				lock_id=self.kwargs['pk']
			).latest('uploaded_at')
			context['user_file_url'] = user_file.file.url
			context['user_file_created_at'] = user_file.uploaded_at
		except Exception as e:
			context['user_file_url'] = "#"
			context['user_file_created_at'] = ""
		try:
			keys = RegisterKey.objects.all().filter(lock_id=self.kwargs['pk'], is_master=True)
			keys_list = []
			for key in keys:
				keys_list.append(key.code)
			context['keys'] = keys_list
		except Exception as e:
			context['keys'] = ""
		return context


@method_decorator(login_required, name='dispatch')
class IncomingDetailView(DetailView):
	model = LockPurchaseRequests
	context_object_name = 'incoming_message'
	template_name = 'manufacturing/incoming_list.html'


@login_required
def lock_create(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LockCreateForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			lock = RegisterLock(
				description=form.cleaned_data["description"],
				firmware=form.cleaned_data["firmware"],
				version=form.cleaned_data["version"],
				current_type=form.cleaned_data["type"],
				current_stage=form.cleaned_data["stage"],

			)

			lock.save()
			lock_with_manual = LockWithManuals(
				lock=lock,
				manual=form.cleaned_data["manual"]
			)
			lock_with_manual.save()
			return HttpResponseRedirect(reverse('manufacturing-lock-detail', args=(lock.pk,)))
	else:
		form = LockCreateForm()
	return render(request, 'manufacturing/lock_create.html', {'form': form})


class LockUpdateView(LoginRequiredMixin, UpdateView):
	model = RegisterLock
	form_class = LockUpdateManufacturingForm
	template_name = 'manufacturing/lock_update.html'

	def get_context_data(self, **kwargs):
		context = super(LockUpdateView, self).get_context_data(**kwargs)
		try:
			lwm = LockWithManuals.objects.all().filter(
			lock_id=self.object.id
			).latest('uploaded_at')
			man = lwm.manual
			form_final = LockUpdateManufacturingForm(
				instance=self.object,
				initial={
					'manual': man,
					'description': self.object.description,
					'current_stage': self.object.current_stage,
					'current_type': self.object.current_type,
					'is_approved': self.object.is_approved,
				})
		except LockWithManuals.DoesNotExist:
			form_final = LockUpdateManufacturingForm(
				instance=self.object,
				initial={
					'description': self.object.description,
					'current_stage': self.object.current_stage,
					'current_type': self.object.current_type,
					'is_approved': self.object.is_approved,
				})

		context['form'] = form_final

		return context

	def post(self, request, *args, **kwargs):
		"""
		Handle POST requests: instantiate a form instance with the passed
		POST variables and then check if it's valid.
		"""
		form = self.get_form()
		if form.is_valid():
			try:
				lwm = LockWithManuals.objects.all().filter(
					lock_id=self.object.id
				).latest('uploaded_at')
				lwm.manual_id = form.cleaned_data['manual']
				lwm.save()
			except Exception as e:
				lwm = LockWithManuals(
					manual_id=form.cleaned_data['manual'],
					lock_id=self.kwargs['pk']
				)
				lwm.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

@login_required
def key_create(request, pk):
		# create a form instance and populate it with data from the request:
	if RegisterKey.objects.all().filter(lock_id=pk, is_master=True).exists():
		return render(request, 'manufacturing/key_error.html')
	else:
		key = RegisterKey(
			is_master=True,
			access_stop=datetime.datetime(2099, 12, 31, 23, 59, 59),
			access_start=datetime.datetime.now(),
			lock_id=pk,
			created_manually=True
		)
		key.save()
	return HttpResponseRedirect(reverse('manufacturing-lock-detail', args=(pk,)))


class KeyUpdateView(LoginRequiredMixin, UpdateView):
	model = RegisterKey
	form_class = MasterKeyUpdateManufacturingForm
	template_name = 'manufacturing/master_key_update.html'

	def get_queryset(self):
		return RegisterKey.objects.all().filter(
			lock_id=self.kwargs['pk'],
			is_master=True
		)

	def get_context_data(self, **kwargs):
		context = super(KeyUpdateView, self).get_context_data(**kwargs)
		context['lock_id'] = self.kwargs['pk']
		return context

	def form_valid(self, form):
		self.object = form.save()
		return super().form_valid(form)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

		return super().post(request, *args, **kwargs)

	def get_object(self, queryset=None):
		try:
			instance_key = RegisterKey.objects.using('lr_backend_main').all().filter(
				lock_id=self.kwargs['pk'], is_master=True
			).latest('updated_at')
			return instance_key
		except Exception as e:
			raise Http404

	def get_success_url(self):
		return reverse('manufacturing-lock-detail', args=(self.kwargs['pk'],))


class LockDeleteView(LoginRequiredMixin, DeleteView):
	model = RegisterLock
	template_name = 'manufacturing/registerlock_confirm_delete.html'
	success_url = '/manufacturing/locks/'


@login_required
def refresh_user_docs(request, pk):
	try:
		instance_docs = LockGeneratedUserFiles.objects.using('lr_backend_main').all().filter(
			lock_id=pk
		).latest('uploaded_at')
		instance_docs.delete()
	except LockGeneratedUserFiles.DoesNotExist:
		instance_docs = None
	try:
		instance_lock = RegisterLock.objects.get(pk=pk)
	except RegisterLock.DoesNotExist:
		raise Http404
	try:
		instance_key = RegisterKey.objects.using('lr_backend_main').all().filter(
			lock_id=pk, is_master=True
		).latest('updated_at')
		key_code = instance_key.code
	except RegisterKey.DoesNotExist:
		key_code = "NOT PROVIDED"

	if str(instance_lock.version) == '1':
		version = 'Ethernet'
	elif str(instance_lock.version) == '2':
		version = 'Wi-Fi'
	else:
		version = 'Custom'

	generated_file = PdfGenerator(
		data={
			"linking_code": instance_lock.linking_code,
			"hash_id": instance_lock.hash_id,
			"version": version,
			"firmware": instance_lock.firmware,
			"uuid": instance_lock.uuid,
			"created_at": instance_lock.created_at,
			"keys": key_code
		},
		pdf_template_path='pdf_generator/owner_file.html').generate()
	filename = "PDF_USER_GUIDE{}.pdf".format(str(instance_lock.id))
	db_gen = LockGeneratedUserFiles(
		filename=filename,
		lock=instance_lock,
		file=File(BytesIO(generated_file), name=filename))
	db_gen.save()

	return HttpResponseRedirect(reverse('manufacturing-lock-detail', args=(pk,)))
