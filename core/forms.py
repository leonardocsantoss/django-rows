# -*- coding: utf-8 -*-
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

import os, rows, requests
import cStringIO as StringIO
from io import BytesIO


class ConvertForm(forms.Form):

    TYPE_CHOICES = (
        ('html', 'html'),
        ('csv', 'csv'),
        ('xls', 'xls'),
        ('txt', 'txt'),
    )

    convert_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    convert_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    type_to = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}))

    def clean_convert_file(self):
        convert_file = self.cleaned_data.get('convert_file')
        convert_url = self.cleaned_data.get('convert_url')
        if not convert_url and not convert_file:
            raise forms.ValidationError(u'Select a file or insert a url.')

        if not convert_url and convert_file:
            if not convert_file.name.split('.')[-1] in [t[0] for t in self.TYPE_CHOICES]:
                raise forms.ValidationError(u'The accepted formats is %s. Send your file in one of these formats.' % u', '.join([t[0] for t in self.TYPE_CHOICES]))
            if convert_file.size/1024 > 1024:
                raise forms.ValidationError(u'The maximum size is 1MB.')
            return convert_file

    def convert(self):

        convert_url = self.cleaned_data.get('convert_url')
        convert_file = self.cleaned_data.get('convert_file')
        type_to = self.cleaned_data.get('type_to')

        if convert_file:
            path = os.path.join(settings.MEDIA_ROOT, default_storage.save(convert_file.name, ContentFile(convert_file.read())))
            convert_type = convert_file.name.split('.')[-1]
            # Import
            data = getattr(rows, 'import_from_%s' % convert_type)(path)
            # Export
            result = StringIO.StringIO()
            getattr(rows, 'export_to_%s' % type_to)(data, result)

            os.unlink(path)
            return result
        else:
            path = BytesIO(requests.get(convert_url).content)
            convert_type = 'html'

            # Import
            data = rows.import_from_html(path, preserve_html=True)
            # Export
            result = StringIO.StringIO()
            getattr(rows, 'export_to_%s' % type_to)(data, result)

            return result

