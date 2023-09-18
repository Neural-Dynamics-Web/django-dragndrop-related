# region				-----External Imports-----
from django.contrib.auth.mixins import PermissionRequiredMixin
import django
import typing
# endregion


class DragAndDropView(
        django.views.generic.edit.ProcessFormView,
        django.views.generic.edit.FormMixin,
        django.views.generic.DetailView,
        PermissionRequiredMixin
    ):

    def get_form_class(self) -> django.forms.ModelForm:
        form_fields = {}
        form_fields[self.kwargs['related_model_field_name']] = django.forms.FileField()
        
        return type('DragAndDropForm', (django.forms.Form,), form_fields)
    

    def get_permission_required(self) -> typing.Tuple[str]:
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        return ("{app_label}.change_{model_name}", )

    
    def form_valid(self, 
            form: django.forms.ModelForm
        ) -> django.http.HttpResponse:
        related_model_order_field_name =\
            self.kwargs['related_model_order_field_name']
            
        related_manager_field_name =\
            self.kwargs['related_manager_field_name']
        
        related_model_field_name =\
            self.kwargs['related_model_field_name']
        

        related_manager = getattr(self.object, related_manager_field_name)
        file = self.request.FILES.get(related_model_field_name)

        with django.db.transaction.atomic():
            add_kwargs = {}
            add_kwargs[related_model_field_name] = file

            if related_model_order_field_name:
                aggregation_name = f"{related_model_order_field_name}__max"
                order = (
                    related_manager.aggregate(
                        django.db.models.Max(related_model_order_field_name)
                    )[aggregation_name] or 0
                ) + 1
                
                add_kwargs[related_model_order_field_name] = order

            object = related_manager.create(**add_kwargs)

            file = getattr(object, related_model_field_name)
            
            reverse_url = django.urls.reverse(
                viewname="dragndrop-delete", 
                args=[
                    object._meta.model_name,
                    object._meta.app_label,
                    object.id
                ]
            )

            data = {
                "name": file.name.split("/")[-1],
                "delete_url": reverse_url,
                "size": file.size,
                "url": file.url,
                "id": object.id
            }

            return django.http.JsonResponse(
                data=data
            )


    def get(self, 
            request: django.http.HttpRequest, 
            *args, **kwargs
        ) -> django.http.HttpResponse:
        # ? Override default behaviour of get method

        self.object = self.get_object()
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        urlpattern = f"admin:{app_label}_{model_name}_change"

        return django.http.HttpResponseRedirect(
            django.urls.reverse(
                kwargs={'object_id': self.object.pk},
                viewname=urlpattern,
            )
        )


    def post(self, 
            request: django.http.HttpRequest, 
            *args, **kwargs
        ) -> django.http.HttpResponse:

        self.object = self.get_object()
        
        return super().post(
            request=request, 
            *args, **kwargs
        )


def delete(
        request: django.http.HttpRequest, 
        model_name: typing.AnyStr,
        app_label: typing.AnyStr, 
        id: typing.Any
    ) -> django.http.HttpResponse:
    # ? Add support for any model in database
    # ? via apps.get_model function

    model = django.apps.apps.get_model(
        model_name=model_name,
        app_label=app_label
    )
    
    data = django.shortcuts\
        .get_object_or_404(
            klass=model, 
            id=id
        ).delete()

    return django.http.HttpResponse(
        status=200
    )