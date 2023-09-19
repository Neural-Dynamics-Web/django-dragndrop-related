# region				-----External Imports-----
import django
import typing
import json
# endregion


def display(
        short_description: typing.AnyStr,
        relation_manager: typing.AnyStr,
        relation_field: typing.AnyStr,

        template: typing.AnyStr = "dragndrop.html",
        empty_value: typing.AnyStr = "-",
        ordering: typing.AnyStr = None
    ) -> typing.Callable:
    
    def wrapper_of_wrapper(function: typing.Callable)\
        -> typing.Callable:

        def default_wrapper(self, 
                instance: django.db.models.Model
            ) -> typing.Any:

            # ? Generate context for appropriate relation
            context = {
                "related_model_field_name": relation_field,
                "change_url_for_relation_model": None,
                "relation": relation_manager,
                "object_id": None,
                "preloaded": [],
                "add": True
            }

            # ? If object exists then add url
            # ? for file uploading
            if instance.id:
                model_name = self.model._meta.model_name
                app_label = self.model._meta.app_label

                if django.conf.settings.USE_I18N:
                    url = f"/en/admin/{app_label}/{model_name}/{instance.id}"\
                        + f"/drag-and-drop/{relation_manager}"
                else:
                    url = f"/admin/{app_label}/{model_name}/{instance.id}"\
                        + f"/drag-and-drop/{relation_manager}"
                
                context["change_url_for_relation_model"] = url


            # ? If object exists then add
            # ? preloaded objects
            if instance.id:
                related_objects = getattr(
                    self.model.objects.get(id=instance.id),
                    relation_manager
                ).all()

                objects = []
                for object in related_objects:
                    reverse_url = django.urls.reverse(
                        viewname="dragndrop-delete", 
                        args=[
                            object._meta.model_name,
                            object._meta.app_label,
                            object.id
                        ]
                    )
                    file = getattr(object, relation_field)

                    # ? Collect necessary information
                    objects.append(
                        {
                            "name": file.name.split("/")[-1],
                            "delete_url": reverse_url,
                            "size": file.size,
                            "url": file.url,
                            "id": object.id
                        }
                    )

                context["preloaded"] =\
                    django.utils.safestring\
                        .mark_safe(
                            s=json.dumps(
                                objects
                            )
                        )
            
            # ? If object exists then add
            # ? object_id to template
            if instance.id:
                context["object_id"] = instance.id
                context["add"] = False
            
            html =  django.template.loader\
                .render_to_string(
                    template_name=template,
                    request=self.request,
                    context=context
                )
            
            return html
        
        default_wrapper.empty_value_display =\
            empty_value
        
        default_wrapper.short_description =\
            short_description

        default_wrapper.relation_manager =\
            relation_manager

        default_wrapper.relation_field =\
            relation_field

        default_wrapper.ordering =\
            ordering

        return default_wrapper
    return wrapper_of_wrapper