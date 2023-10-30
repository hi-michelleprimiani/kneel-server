import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_create, db_delete


class OrdersView():

    def get(self, handler, pk):
        parsed_url = handler.parse_url(handler.path)
        if pk != 0:
            # Retrieve a single order by ID
            dictionary_order = self._get_single_order(pk, parsed_url)
            serialized_order = json.dumps(dictionary_order)
            return handler.response(serialized_order, status.HTTP_200_SUCCESS.value)
        else:
            # Retrieve an array of all orders with optional resource expansion
            serialized_orders = json.dumps(
                self._get_all_orders(parsed_url, pk))
            return handler.response(serialized_orders, status.HTTP_200_SUCCESS.value)

    def create(self, handler, data):
        # Create a new order
        object_id = self._create_order(data)
        if object_id > 0:
            response_sql = "SELECT o.id, o.metalId, o.styleId, o.sizeId FROM Orders o WHERE o.id = ?"
            query_response = db_get_single(response_sql, object_id)
            serialized_order = {
                "id": query_response["id"],
                "metalId": query_response['metalId'],
                "styleId": query_response["styleId"],
                "sizeId": query_response['sizeId']
            }
            post_response = json.dumps(serialized_order)
            return handler.response(post_response, status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

    def update(self, handler):
        # Update method is not supported (HTTP 405)
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def delete(self, handler, pk):
        # Delete an order by ID
        number_of_row_deleted = self._delete_order(pk)
        if number_of_row_deleted > 0:
            response_body = f"Order #{pk} Deleted"
            return handler.response(response_body, status.HTTP_200_SUCCESS.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def _get_single_order(self, order_id, parsed_url):
        single_sql = """SELECT
            o.id,
            o.styleId,
            o.sizeId,
            o.metalId
            FROM Orders o
            WHERE o.id = ?
            """
        query_results = db_get_single(single_sql, order_id)
        dictionary_order = dict(query_results)

        for resource in parsed_url.get('query_params', {}).get('_expand', []):
            if hasattr(self, f"_expand_{resource}"):
                expansion_method = getattr(self, f"_expand_{resource}")
                expanded_data = expansion_method(dictionary_order)
                dictionary_order[resource] = expanded_data

        return dictionary_order

    def _get_all_orders(self, parsed_url, pk):
        all_sql = """
        SELECT
        o.id,
        o.styleId,
        o.metalId,
        o.sizeId,
        Styles.id AS style_id,
        Styles.style AS style,
        Styles.price AS style_price,
        Metals.id AS metal_id,
        Metals.metal AS metal,
        Metals.price AS metal_price,
        Sizes.id AS size_id,
        Sizes.carets AS carets,
        Sizes.price AS size_price
        FROM Orders o
        LEFT JOIN Styles ON o.styleId = Styles.id
        LEFT JOIN Metals ON o.metalId = Metals.id
        LEFT JOIN Sizes ON o.sizeId = Sizes.id
        GROUP BY o.id
        """
        orders_sql = db_get_all(all_sql, pk)
        orders = {}

        for row in orders_sql:
            order_id = row['id']
            if order_id not in orders:
                orders[order_id] = {
                    "id": order_id,
                    "styleId": row['styleId'],
                    "metalId": row['metalId'],
                    "sizeId": row['sizeId'],
                }
                if 'query_params' in parsed_url and '_expand' in parsed_url['query_params']:
                    for resource in parsed_url['query_params']['_expand']:
                        if hasattr(self, f"_expand_{resource}"):
                            expansion_method = getattr(
                                self, f"_expand_{resource}")
                            expanded_data = expansion_method(row)
                            orders[order_id][resource] = expanded_data

        return list(orders.values())

    def _create_order(self, data):
        create_sql = """
        INSERT INTO Orders ('metalId', 'styleId', 'sizeId') VALUES (?, ?, ?)
        """
        object_id = db_create(
            create_sql, (data['metalId'], data['styleId'], data['sizeId']))
        return object_id

    def _delete_order(self, order_id):
        number_of_row_deleted = db_delete(
            "DELETE FROM Orders where id = ?", order_id)
        return number_of_row_deleted

    def _expand_metal(self, order):
        fk = order.get('metalId')
        if fk is not None:
            expand_sql = """SELECT
            m.id,
            m.metal,
            m.price
            FROM Metals m
            WHERE m.id = ?
            """
            metal_data = db_get_single(expand_sql, fk)
            metal = {
                "id": metal_data['id'],
                "metal": metal_data['metal'],
                "price": metal_data['price']
            }
            return metal
        return None

    def _expand_size(self, order):
        fk = order.get('sizeId')
        if fk is not None:
            expand_sql = """SELECT
            s.id,
            s.carets,
            s.price
            FROM Sizes s
            WHERE s.id = ?
            """
            size_data = db_get_single(expand_sql, fk)
            size = {
                "id": size_data['id'],
                "carets": size_data['carets'],
                "price": size_data['price']
            }
            return size
        return None

    def _expand_style(self, order):
        fk = order.get('styleId')
        if fk is not None:
            expand_sql = """SELECT
            s.id,
            s.style,
            s.price
            FROM Styles s
            WHERE s.id = ?
            """
            style_data = db_get_single(expand_sql, fk)
            style = {
                "id": style_data['id'],
                "style": style_data['style'],
                "price": style_data['price']
            }
            return style
        return None
