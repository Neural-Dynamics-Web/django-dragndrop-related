# region				-----External Imports-----
import django
import typing
# endregion

# region				-----Internal Imports-----
from .. import views
# endregion


class DragAndDropModelAdmin(object):
    relations_information = []


    def __init__(self, *args, **kwargs)\
        -> None:
        super(DragAndDropModelAdmin, self)\
            .__init__(*args, **kwargs)

        # ? Find all dragndrop_ functions in the current class
        # ? and get from them necessary information
        #? to initialize components
        dragndrop_objects = list(
            filter(
                lambda item: item.startswith("dragndrop_"),
                dir(self)
            )
        )

        for object in dragndrop_objects:
            object = getattr(self, object, None)
            if object:
                self.relations_information.append(
                    {
                        "manager": object.relation_manager,
                        "field": object.relation_field,
                        "ordering": object.ordering
                    }
                )

    
    def get_urls(self) -> typing.List[typing.Any]:
        # ? Generate view for uploading
        # ? different relayional files
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        

        related_models_information =\
            self.get_related_model_info()\
                ["relation_models_information"]

        routes = []
        for information in self.relations_information:
            kwargs = related_models_information[information["manager"]]

            route = f"<int:pk>/drag-and-drop/{information['manager']}"

            name = f"{app_label}_{model_name}_drag_and_drop"\
                 + f"_{information['manager']}"

            view = self.admin_site.admin_view(
                views.DragAndDropView.as_view(model=self.model)
            )
            
            routes.append(
                django.urls.path(
                    kwargs=kwargs,
                    route=route,
                    view=view,
                    name=name
                )
            )

        return routes + super().get_urls()


    def get_related_model_info(self,
            object_id: typing.Any = None
        ) -> typing.Dict:

        # ? Collect necessary information abour relation
        # ? model such as vebose_name and .etc
        relation_models_information = {}

        for information in self.relations_information:
            related_model =\
                getattr(self.model, information["manager"])\
                    .field.model

            relation_models_information[information["manager"]] = {
                'change_url_for_relation_model':
                    f'drag_and_drop_{information["manager"]}',
                'related_model_name_plural':
                    related_model._meta.verbose_name_plural,
                'related_model_name':
                    related_model._meta.verbose_name,
                'related_model_order_field_name':
                    information["ordering"],
                'related_manager_field_name':
                    information["manager"],
                'related_model_field_name':
                    information["field"],
                'related_model':
                    related_model
            }

            if object_id:
                model_name = self.model._meta.model_name
                app_label = self.model._meta.app_label
                manager = information["manager"]

                url = f"/admin/{app_label}/{model_name}"\
                    + f"/{object_id}/drag-and-drop"\
                    + f"{manager}"

                relation_models_information[manager]\
                    .update(
                        change_url_for_relation_model=url
                    )
        
        return {
            "relation_models_information":\
                relation_models_information
        }

    
    def changelist_view(self, 
            request: django.http.HttpRequest,

            extra_context: typing.Dict = {}
        ) -> django.http.HttpResponse:

        # ? Add request to the current class
        # ? it will be used in the collected
        # ? methods for components
        self.request = request

        return super().changelist_view(
            extra_context=extra_context,
            request=request
        )

    
    def change_view(self, 
            request: django.http.HttpRequest, 
            object_id: typing.Any,

            extra_context: typing.Dict = {},
            form_url: typing.AnyStr = ""
        ) -> django.http.HttpResponse:

        # ? Add request to the current class
        # ? it will be used in the collected
        # ? methods for components
        self.request = request

        return super().change_view(
            extra_context=extra_context,
            object_id=object_id,
            form_url=form_url,
            request=request
        )
    

    def add_view(self, 
            request: django.http.HttpRequest,

            extra_context: typing.Dict = {},
            form_url: typing.AnyStr = "",
        ) -> django.http.HttpResponse:

        # ? Add request to the current class
        # ? it will be used in the collected
        # ? methods for components
        self.request = request

        return super().add_view(
            extra_context=extra_context,
            form_url=form_url,
            request=request
        )