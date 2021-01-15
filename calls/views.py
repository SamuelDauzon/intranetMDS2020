from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect


# Create your views here.
from .forms import NewCallForm
from .models import Call
from users.views import is_teammember


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


@user_passes_test(is_teammember)
def call_list(request):
    calls = Call.objects.filter(teammember = request.user.teammember).order_by("-solved", "-created")
    return render(
        request,
        'calls/call_list.html',
        {
            'calls': calls,
        }
    )


@user_passes_test(is_teammember)
def call_edit(request, call_id=None):
    current_instance = None
    if call_id:
        # current_instance = Call.objects.get(id = call_id, teammember = request.user.teammember)
        # Equivalent à la ligne du bas sans la gestion de levée d'exption 404
        current_instance = get_object_or_404(Call, pk = call_id, teammember = request.user.teammember)
    if request.method == 'POST':
        form = NewCallForm(request.POST, instance = current_instance)
        if form.is_valid():
            if not current_instance:
                form.instance.teammember = request.user.teammember
            form.save()
            return HttpResponseRedirect(reverse("calls:call_list"))
    else:
        form = NewCallForm(instance = current_instance)
    return render(
        request,
        'utils/form.html',
        {
            'title': "Appel",
            'form':form,
        }
    )
