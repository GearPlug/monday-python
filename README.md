# monday-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*monday-python* is an API wrapper for monday.com, written in Python.  
This library includes notifications using webhooks.
## Installing
```
pip install monday-python
```
### Usage
```python
from monday.client import Client
client = Client(api_token)
```
Find your API token in your monday.com profile admin settings API section.

### - Get current user
```python
user = client.get_current_user()
```
#### - List Users
```python
users = client.list_users()
```
#### - List workspaces
```python
workspaces = client.list_workspaces()
```
#### - List boards
```python
boards = client.list_boards(workspace_id)
```
#### - List columns
```python
cols = client.list_columns(board_id)
```
### Items
#### - List items
```python
items = client.list_items(board_id)
```
#### - Get items by column values
```python
# The item's state: all, active, archived, or deleted. The default state is active.
items = client.get_items_by_column_values(board_id, column_id, column_value, limit=50, state="active")
```
#### - Create item
```python
# column_values is a dictionary with the following structure:
#    {"column_name": "column_value", "column_name": "column_value"}
item = client.create_item(board_id, item_name: str, column_values: dict = None)
```
### Webhooks
#### - List webhooks
```python
webhooks = client.list_webhooks(board_id)
```
#### - Create webhook
```python
webhook = client.create_webhook(board_id, url, event)
```
To activate a webhook, the URL must return a response to a post request that monday.com will send to verify.  
Read more about it here: https://developer.monday.com/api-reference/docs/webhooks
#### - Delete a webhook
```python
deleted = client.delete_webhook(webhook_id)
```
