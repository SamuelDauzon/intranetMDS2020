from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import UserProfile, TeamMember, Customer, Article

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'display_name', 'newsletter_agreement', )
    list_filter = ['user_type', 'newsletter_agreement', ]
    list_editable = ['display_name', ]
    search_fields = ['username', 'email', 'display_name', ]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', )
    list_filter = []
    list_editable = []
    search_fields = ['title', ]

    # class Meta:
    #     model = Article
    #     widgets = {
    #       'content': SummernoteInplaceWidget(),
    #     }
    #     fields = '__all__'


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(TeamMember)
admin.site.register(Customer)