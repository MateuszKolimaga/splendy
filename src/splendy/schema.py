from drf_spectacular.openapi import AutoSchema as _AutoSchema
from rest_framework.request import is_form_media_type


class AutoSchema(_AutoSchema):
    def map_parsers(self) -> list[str]:
        """
        Return a unique list of media types.

        Overrides the default behaviour to remove form media types as done in ``drf_yasg.utils.get_consumes()``.
        We could have changed DRF's ``DEFAULT_PARSER_CLASSES`` setting but we don't want to inadvertently break things.

        The reason for implementing this hack is to work around broken client generation from ``swagger-codegen`` which
        is used by editor.swagger.io and seems to be incapable of handling multiple media types in request bodies. As
        this may be used by clients, we'll tweak this even though our specification is perfectly valid when unaltered.

        It may be better to steer clients to use ``openapi-generator`` instead. This doesn't support multiple media
        types in the generated client code, but it doesn't generate invalid output by using the first available media
        type (which is ``application/json`` based on the default value of ``DEFAULT_PARSER_CLASSES``.

        See the following links for additional information:

        - https://github.com/swagger-api/swagger-codegen/issues/8191
        - https://github.com/OpenAPITools/openapi-generator/issues/2668
        - https://openapi-generator.tech/
        """
        media_types = super().map_parsers()
        non_form_media_types = [x for x in media_types if not is_form_media_type(x)]
        return non_form_media_types if non_form_media_types else media_types
