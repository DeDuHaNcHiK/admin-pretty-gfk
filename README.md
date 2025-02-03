# admin_pretty_gfk

Custom Django admin mixin and widgets for handling generic foreign keys (GFKs) more intuitively.

## Features
- **PrettyGFKModelAdminMixin**: A mixin that enhances Django's admin interface for models with GFKs.
- **ForeignKeyContentIdWidget**: A raw ID widget with a fallback URL to prevent errors.
- **ContentTypeSelect**: A dropdown widget that dynamically updates related object selection and resets the foreign key field when the content type changes.

## Installation
```sh
pip install admin_pretty_gfk
```

## Usage
### Import and Use in ModelAdmin
#### Using the Widget
```python
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
```

#### Using the Mixin
```python
from admin_pretty_gfk.mixins import PrettyGFKModelAdminMixin
from django.contrib import admin

class AdvertAdmin(PrettyGFKModelAdminMixin, admin.ModelAdmin):
    pass
```

#### Registering Models
```python
admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Rent)
admin.site.register(Advert, AdvertAdmin)
```

## How It Works
1. `PrettyGFKModelAdminMixin` automates form handling for models with GFKs.
2. `ContentTypeSelect` updates object selection dynamically when the content type changes.
3. `ForeignKeyContentIdWidget` ensures proper URL handling for related objects.

## License
This project is licensed under the MIT License.

