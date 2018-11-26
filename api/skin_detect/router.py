from flask_apispec import doc, MethodResource
from flask_apispec import use_kwargs
from marshmallow import fields


class FileField(fields.Raw):
    pass


@doc(description="send image api", tags=['Skin Detect'])
class ImageEndPoint(MethodResource):

    @use_kwargs({"image": FileField()})
    def post(self):
        return {}