from django import forms

from users.forms import ModelFormWithSubmit
from users.models import TeamMember
from .models import Call, CallTag


class NewCallForm(ModelFormWithSubmit):

    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=CallTag.objects.all(),
        required=False,
        )

    class Meta:
        model = Call
        fields = ('title', 'customer', 'call_category', 'tags', 'content', 'solved', )

class NewCustomerCallForm(NewCallForm):

    class Meta:
        model = Call
        fields = ('title', 'call_category', 'tags', 'content', )

class CustomerCallEditForm(ModelFormWithSubmit):

    class Meta:
        model = Call
        fields = ('content', )

class CallEditTeammemberForm(ModelFormWithSubmit):

    def restrict(self, user):
        if not user.is_superuser:
            print(TeamMember.objects.filter(teammember_id=user.id).query)
            self.fields['teammember'].queryset = TeamMember.objects.filter(teammember_id=user.id)

    class Meta:
        model = Call
        fields = ('teammember', )

class CallRatingForm(ModelFormWithSubmit):

    class Meta:
        model = Call
        fields = ('rating', ) 


        
