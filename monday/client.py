import json

import requests

from monday.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.monday.com/v2"
    headers = {"Content-Type": "application/json"}

    def __init__(self, api_key):
        self.headers.update({"Authorization": api_key})

    def get_current_user(self):
        body = {"query": "query { me { is_guest created_at name id}}"}
        return self.post(json=body)

    def list_users(self):
        body = {"query": "query { users { id email name phone account { id name slug } }}"}
        return self.post(json=body)

    def list_workspaces(self):
        body = {"query": "query { workspaces { id name kind description }}"}
        return self.post(json=body)

    def list_boards(self, workspace_id):
        body = {
            "query": f"query {{ boards (workspace_ids: {workspace_id}) {{ name state id permissions columns {{ id title type }} }}}}"
        }
        return self.post(json=body)

    def list_columns(self, board_id):
        body = {"query": f"query {{boards (ids: {board_id}) {{ columns {{ id title type settings_str }}}}}}"}
        return self.post(json=body)

    def list_items(self, board_id):
        body = {
            "query": f"query {{boards (ids: {board_id}) {{ items {{ id name created_at column_values {{title text}} }}}}}}"
        }
        return self.post(json=body)

    def get_item(self, item_id):
        body = {
            "query": f"query {{items (ids: {item_id}) {{ id name created_at column_values {{ title text }}  }}}}"
        }
        return self.post(json=body)


    def get_items_by_column_values(self, board_id, column_id, value, limit: int = 50, state: str = "active"):
        """
        Default limit is 50.
        The item's state: all, active, archived, or deleted. The default state is active.
        """
        query = f"""
            query {{
                items_by_column_values (
                    board_id: {board_id},
                    column_id: "{column_id}",
                    column_value: "{value}",
                    limit: {limit},
                    state: {state}
                ) {{ id name created_at column_values {{title text}} }}}}
            """
        body = {"query": query}
        return self.post(json=body)

    def create_item(self, board_id, item_name: str, column_values: dict = None):
        """
        Creates an item inside a given board.
        column_values is a dictionary with the following structure:
            {"column_id": "column_value", "column_id": "column_value"}
        """
        query = "mutation ($boardId: Int!, $myItemName: String!, $columnVals: JSON!) { create_item (board_id: $boardId, item_name: $myItemName, column_values:$columnVals) { id } }"
        variables = {
            "boardId": int(board_id),
            "myItemName": item_name,
            "columnVals": json.dumps(column_values),
        }
        body = {"query": query, "variables": variables}
        return self.post(json=body)

    def update_item(self, board_id, item_id, column_values: dict):
        """
        column_values is a dictionary with the following structure:
            {"column_id": "column_value", "column_id": "column_value"}
        """
        query = """
            mutation ($boardId: Int!, $itemId: Int!, $columnVals: JSON!) {
                change_multiple_column_values (item_id: $itemId, board_id: $boardId, column_values: $columnVals) 
                    { id }
            }
        """
        variables = {"boardId": int(board_id), "itemId": int(item_id), "columnVals": json.dumps(column_values)}
        body = {"query": query, "variables": variables}
        return self.post(json=body)

    def list_webhooks(self, board_id):
        body = {"query": f"query {{ webhooks(board_id: {board_id}) {{ id event config }}}}"}
        return self.post(json=body)

    def create_webhook(self, board_id: int, url: str, event: str, config: str = None):
        query = f'mutation {{ create_webhook (board_id: {board_id}, url: "{url}", event: {event}) {{ id }} }}'
        body = {"query": query}
        return self.post(json=body)

    def delete_webhook(self, webhook_id):
        body = {"query": f"mutation {{ delete_webhook (id: {webhook_id}) {{ id board_id }} }}"}
        return self.post(json=body)

    def get(self, **kwargs):
        response = self.request("GET", **kwargs)
        return self.parse(response)

    def post(self, **kwargs):
        response = self.request("POST", **kwargs)
        return self.parse(response)

    def request(self, method, headers=None, **kwargs):
        if headers:
            self.headers.update(headers)
        return requests.request(method, self.URL, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
