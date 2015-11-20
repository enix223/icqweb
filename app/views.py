from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from django.http import HttpResponse
from django.contrib import messages
import json

from app.models import UserProfile, Package, UserPackageRel, Order


class JSONResponseMixin(object):
    """
    A mixin that used to render a JSON response.
    """

    def render_to_json(self, context, **response_kwargs):
        """"
        Returns a JSON response, transforming 'context' to make the payload
        """
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class UserCreateForm(UserCreationForm):
    """User signon form"""
    promo_code = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=255)

    def clean_promo_code(self):
        # TODO Add promo code logic
        return self.cleaned_data.get('promo_code')

    def clean_last_name(self):
        # TODO Add last name
        return self.cleaned_data.get('last_name')

    def save(self, commit=True):
        """ Override save method """
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['username']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserSignonView(JSONResponseMixin, CreateView):
    """ User signon view """
    template_name = 'registration/signon.html'
    form_class = UserCreateForm

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            context['success_url'] = self.get_success_url()
            form.save()
            messages.info(
                self.request,
                'Congratulations. User created successfully.')
        except Exception, e:
            messages.error(
                self.request,
                'Oops! Register failed. Please try later.')
            messages.debug(
                self.request,
                'Error: [%s]' % str(e)
            )
        return SingleObjectTemplateResponseMixin.render_to_response(self, context)


class UserConsoleView(TemplateView):
    """ User console """
    template_name = 'user/console.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserConsoleView, self).dispatch(*args, **kwargs)


class UserProfileView(TemplateView):
    """ User Profile view """
    template_name = 'user/profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileView, self).dispatch(*args, **kwargs)


class PackageListView(ListView):
    """Pricing view (list all package"""
    template_name = 'packages/list.html'
    context_object_name = 'packages_list'
    model = Package


class PackageUpgradeForm(forms.Form):
    package = forms.IntegerField()


class PackageUpgradeView(TemplateView):
    template_name = 'user/upgrade.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PackageUpgradeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'package' not in request.GET:
            return redirect('pricing')
        else:
            form = PackageUpgradeForm(request.GET)
            package = get_object_or_404(Package, pk=request.GET['package'])
            order = Order.objects.create(user=request.user, package=package)
            return render(
                request,
                self.template_name, {
                    'form': form,
                    'package': package,
                    'order': order,
                }
            )


class UserVPNPasswdChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']


class UserVPNPasswdChangeView(UpdateView):
    form_class = UserVPNPasswdChangeForm
    template_name = 'user/profile.html'
    model = UserProfile
    queryset = UserProfile.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserVPNPasswdChangeView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        up = UserProfile.objects.get(user=self.request.user)
        up.passwd = form.cleaned_data['passwd']
        up.save()
        messages.info(self.request, 'Update successfully.')
        return super(UserVPNPasswdChangeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user-profile')

    def get_context_data(self, **kwargs):
        context = super(UserVPNPasswdChangeView, self).get_context_data(**kwargs)
        context['vpn_form'] = context.get('form', '')
        del context['form']
        return context
