# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.http import HttpResponse

from forms import ConvertForm


class ConvertView(FormView):
    template_name = 'convert.html'
    form_class = ConvertForm

    def form_valid(self, form):
        result = form.convert()

        if form.cleaned_data.get('convert_file'):
            filename = u'%s.%s' % (
                '.'.join(form.cleaned_data.get('convert_file').name.split('.')[:-1]),
                form.cleaned_data.get('type_to')
            )
        else:
            filename = u'file.%s' % form.cleaned_data.get('type_to')

        response = HttpResponse(result.getvalue(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'filename=%s' % filename
        return response