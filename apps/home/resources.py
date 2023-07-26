from import_export import resources
from .models import *


class MyModelResource(resources.ModelResource):
    class Meta:
        model = CaracterisationPanification

