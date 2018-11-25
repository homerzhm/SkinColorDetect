from flask_apispec import doc, MethodResource


@doc(description="send image api", tags=['Skin Detect'])
class ImageEndPoint(MethodResource):

    def post(self):
        return {}
