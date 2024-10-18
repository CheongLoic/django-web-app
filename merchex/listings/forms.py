from django import forms
from listings.models import Band

class ContactUsForm(forms.Form):
   name = forms.CharField(required=False) # require=False ==> champ facultatif
   email = forms.EmailField()
   message = forms.CharField(max_length=1000)


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = '__all__' # supprimez cette ligne
        # exclude = ('active', 'official_homepage')  # ajoutez cette ligne

