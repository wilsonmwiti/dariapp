from django import forms
from .models import Stake

class IstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("user", "marketselection", "amount", "bet_on_real_account")
