import json
from nss_handler import status
from repository import db_get_single, db_get_all


class StylesView():
    def get(self, handler, pk):

        if pk != 0:
            sql = "SELECT sty.id, sty.style, sty.price FROM Styles sty WHERE sty.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_style = json.dumps(dict(query_results))

            return handler.response(serialized_style, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT sty.id, sty.style, sty.price FROM Styles sty"
            query_results = db_get_all(sql, pk)
            metals = [dict(row) for row in query_results]
            serialized_styles = json.dumps(metals)

            return handler.response(serialized_styles, status.HTTP_200_SUCCESS.value)

    def create(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def update(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def delete(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
