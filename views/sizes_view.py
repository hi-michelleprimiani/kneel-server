import json
from nss_handler import status
from repository import db_get_single, db_get_all


class SizeView():

    def get(self, handler, pk):
        if pk != 0:
            sql = """
                SELECT
                    size.id,
                    size.caret,
                    size.price
                FROM Sizes size 
                WHERE size.id = ?
                """
            query_results = db_get_single(sql, pk)
            serialized_size = json.dumps(dict(query_results))

            return handler.response(serialized_size, status. HTTP_200_SUCCESS.value)

        else:
            sql = "SELECT siz.id, siz.caret, siz.price FROM Sizes siz"
            query_results = db_get_all(sql, pk)
            metals = [dict(row) for row in query_results]
            serialized_sizes = json.dumps(metals)

            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)

    def create(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def update(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def delete(self, handler):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
