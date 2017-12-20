from django.conf.urls import url
import inspect
import models
from . import views

urlpatterns = []
# Add a new patern for each normal class in models file
for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj) and name[0:2] != '__':
        urlpatterns.append(
            url(
                r'^{}/$'.format(name.lower()),
                views.import_entrypoint_view,
                name='{}import'.format(name.lower())
            )
        )

