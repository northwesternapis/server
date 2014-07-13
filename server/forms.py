from django.forms import ModelForm
from server.models import *

class APIProjectRequestForm(ModelForm):
    class Meta:
        model = APIProjectRequest
        fields = ['owner', 'name', 'description', 'how_long']
