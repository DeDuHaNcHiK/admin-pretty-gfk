from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.utils.safestring import mark_safe


class ForeignKeyContentIdWidget(ForeignKeyRawIdWidget):

    template_name = "widgets/foreign_key_content_id.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if context.get('related_url') is None:
            context['related_url'] = '#'
        return context


class ContentTypeSelect(forms.Select):
    def __init__(self, lookup_id='lookup_id_object_id', raw_fk='id_object_id', attrs=None, choices=()):
        self.lookup_id = lookup_id
        self.raw_fk = raw_fk
        super(ContentTypeSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        output = super(ContentTypeSelect, self).render(name, value, attrs, renderer=None)

        choices = self.choices
        choice_output = ' var %s_choice_urls = {' % (attrs['id'],)
        for choice in choices.queryset:
            try:
                choice_output += '    \'%s\' : \'../../%s/?_to_field=%s\',' % (
                    str(choice.pk),
                    choice.model,
                    choice.model_class()._meta.pk.name
                )
            except:
                pass
        choice_output += '};'

        output += (
                '''<script type="text/javascript">
                (function($) {
                  $(document).ready( function() {
                %(choice_output)s
                    $(\'#%(id)s\').on("change", function (){
                        $(\'#%(fk_id)s\').attr(\'href\',%(id)s_choice_urls[$(this).val()]);
                        $(\'#%(raw_fk)s\').val(\'\');
                        $(\'#%(raw_fk)s\').parent(\'div\').find(\'strong\').text(\'\');
                    });
                  });
                })(django.jQuery);
                </script>''' % {
                    'choice_output': choice_output,
                    'id': attrs['id'],
                    'fk_id': self.lookup_id,
                    'raw_fk': self.raw_fk
                }
        )
        return mark_safe(''.join(output))
