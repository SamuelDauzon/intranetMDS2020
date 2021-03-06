from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponseRedirect

from .forms import NewCallForm, NewCustomerCallForm, CustomerCallEditForm
from .forms import CallEditTeammemberForm, CallRatingForm
from .models import Call
from users.views import is_teammember, is_customer, is_customer_or_teammember


@user_passes_test(is_teammember)
def new_call(request):
    if request.method == 'POST':
        form = NewCallForm(request.POST)
        if form.is_valid():
            form.instance.teammember = request.user.teammember
            form.save()
            return HttpResponseRedirect(reverse("calls:call_list"))
    else:
        form = NewCallForm()
    return render(
        request,
        'utils/form.html',
        {
            'title': "Nouvel Appel",
            'form':form,
        }
    )

@user_passes_test(is_customer_or_teammember)
def call_list(request):
    calls = None
    template_name = ""
    if request.user.is_customer():
        calls = Call.objects.filter(
            customer = request.user.customer,
            ).order_by(
                "-solved",
                "-created",
            )
        template_name = "calls/call_list_customer.html"
    if request.user.is_teammember():
        calls = Call.objects.filter(
            teammember = request.user.teammember,
            ).order_by(
                "-solved",
                "-created",
            )
        template_name = "calls/call_list.html"
    return render(
        request,
        template_name,
        {
            'calls': calls,
        }
    )

@user_passes_test(is_teammember)
def call_edit(request, call_id=None):
    current_instance = None
    if call_id:
        try:
            current_instance = Call.objects.get(
                Q(id = call_id),
                Q(solved = False),
                Q(teammember = request.user.teammember) | Q(teammember__isnull=True),
                )
        except Call.DoesNotExist as e:
            # Redirection
            # 403
            # 404
            pass
    form_class = NewCallForm
    if current_instance and not current_instance.teammember:
        form_class = CallEditTeammemberForm
    if request.method == 'POST':
        form = form_class(request.POST, instance = current_instance)
        if form_class == CallEditTeammemberForm:
            form.restrict(request.user)
        if form.is_valid():
            if not current_instance:
                form.instance.teammember = request.user.teammember
            form.save()
            return HttpResponseRedirect(reverse("calls:call_list"))
    else:
        form = form_class(instance = current_instance)
        if form_class == CallEditTeammemberForm:
            form.restrict(request.user)

    return render(
        request,
        'utils/form.html',
        {
            'title': "Appel",
            'form':form,
        }
    )

@user_passes_test(is_customer)
def new_call_customer(request):
    if request.method == 'POST':
        form = NewCustomerCallForm(request.POST)
        if form.is_valid():
            form.instance.customer = request.user.customer
            form.save()
            return HttpResponseRedirect(reverse("calls:call_list"))
    else:
        form = NewCustomerCallForm()
    return render(
        request,
        'utils/form.html',
        {
            'title': "Nouvelle demande",
            'form':form,
        }
    )


@user_passes_test(is_customer)
def call_edit_customer(request, call_id):
    current_instance = Call.objects.get(id = call_id, customer = request.user.customer)
    if request.method == 'POST':
        form = CustomerCallEditForm(request.POST, instance = current_instance)
        if form.is_valid():
            form.save()
    else:
        form = CustomerCallEditForm(instance = current_instance)
    return render(
        request,
        'utils/form.html',
        {
            'title': "Appel",
            'form':form,
        }
    )


@user_passes_test(is_teammember)
def call_list_no_teammember(request):
    # print(Call.objects.filter(teammember__isnull=True).exclude(solved=True).order_by("-created").query)
    calls = Call.objects.filter(teammember__isnull=True).exclude(solved=True).order_by("-created")
    return render(
        request,
        'calls/call_list.html',
        {
            'calls': calls,
        }
    )

@user_passes_test(is_customer)
def call_rating(request, call_id):
    current_instance = Call.objects.get(id = call_id, customer = request.user.customer, solved = True)
    if request.method == 'POST':
        form = CallRatingForm(request.POST, instance = current_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("calls:call_list"))
    else:
        form = CallRatingForm(instance = current_instance)
    return render(
        request,
        'utils/form.html',
        {
            'title': "Noter la prestation",
            'form':form,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def bad_calls(request, call_id = None):
    calls = Call.objects.filter(
        rating__lte=5
        )
    print(calls.query)
    calls = calls.order_by(
        "-created",
        )
    print(calls.query)
    return render(
        request,
        "calls/call_list.html",
        {
            'calls': calls,
        }
    )



