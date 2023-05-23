import re  
from notion.client import NotionClient  

def enumerate_notion_items(  
  view_url, id_col, created_at_col="created_time", token=None, client=None  
):  
  if client is None:  
    if token is None:  
      token = input("Please provide token: ")  
    client = NotionClient(token_v2=token)  
  view = client.get_collection_view(view_url)  
  items = view.collection.get_rows()  
  sorted_items = sorted(items, key=lambda i: (getattr(i, id_col), getattr(i, created_at_col)))  
  with_id = [item for item in sorted_items if getattr(item, id_col)]  
  without_id = [item for item in sorted_items if not getattr(item, id_col, None)]  
  if len(with_id) == 0:  
    raise Exception("At least one item with id is required, for safety")  
  if not getattr(with_id[0], created_at_col):  
    raise Exception("Item does not have '%s' creation time field" % created_at_col)  
  if len(set(getattr(item, id_col) for item in with_id)) != len(with_id):  
    raise Exception("Duplicate ids detected, please fix manually")  
  prefix, counter_str = re.match("([a-zA-Z\s]*)([0-9]*)", getattr(with_id[-1], id_col)).groups()  
  if not counter_str:  
    raise Exception("At least one item id ending with a number is required")  
  next_counter = int(counter_str) + 1  
  for item in without_id:  
    id_col_value = "%s%s" % (prefix, next_counter)  
    setattr(item, id_col, id_col_value)  
    print('Setting new id value: "%s" for item: %s' % (id_col_value, item.title))  
    next_counter += 1
