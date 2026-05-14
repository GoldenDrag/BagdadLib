from django import forms



class UploadBookForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}),
                                  required=False)
    file = forms.FileField()