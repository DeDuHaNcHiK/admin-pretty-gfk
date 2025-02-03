from admin_pretty_gfk import PrettyGFKModelAdminMixin
from admin_pretty_gfk.widgets import ContentTypeSelect, ForeignKeyContentIdWidget
from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ManyToOneRel

from common.models import Buy, Sell, Rent, Advert


class AdvertModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdvertModelForm, self).__init__(*args, **kwargs)
        try:
            model = self.instance.content_type.model_class()
            model_key = model._meta.pk.name
        except (AttributeError, ObjectDoesNotExist):
            model = self.fields['content_type'].queryset[0].model_class()
            model_key = 'id'
        self.fields['object_id'].widget = ForeignKeyContentIdWidget(
            rel=ManyToOneRel(model_key, model, 'id'),
            admin_site=admin.site
        )

    class Meta:
        model = Advert
        fields = "__all__"
        widgets = {
            'content_type': ContentTypeSelect
        }


class AdvertAdmin(admin.ModelAdmin):
    form = AdvertModelForm


# class AdvertAdmin(PrettyGFKModelAdminMixin, admin.ModelAdmin):
#     pass


admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Rent)
admin.site.register(Advert, AdvertAdmin)
