# region				-----External Imports-----
import django
# endregion

# region				-----Internal Imports-----
from . import views
# endregion


urlpatterns = [
    django.urls.path(
        route='dragndrop/delete/<str:model_name>/<str:app_label>/<int:id>', 
        name="dragndrop-delete",
        view=views.delete
    )
]