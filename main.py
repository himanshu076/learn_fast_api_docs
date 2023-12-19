from fastapi import FastAPI, Query, Path, Body
from constant import ModelName
from data_model import Item, User, Offer, Image
from typing import Annotated

app = FastAPI()


# Path Parameter Learning start ----------
@app.get('/')
async def root():
  return {'message': 'Hello World'}

# @app.get('/items/{item_id}')
# async def read_item(item_id: int):
#   return {'item_id': item_id}

@app.get('/users/me')
async def read_user_me():
  return {"user_id": "the current user"}

@app.get('/users/{user_id}')
async def read_user(user_id: str):
  return {"user_id": user_id}

@app.get('/users')
async def read_users():
  return ["Rick", "Morty"]


@app.get('/users')
async def read_users2():
  return ["Bean", "Elfo"]

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
  if model_name is ModelName.alexnet:
    return {'model_name': model_name, 'message': 'Deep Learning FTW!'}
  if model_name is ModelName.resnet:
    return {"model_name": model_name, "message": "LeCNN all the images"}

  return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Path Parameter Learning end ----------

# *****************************************************************************

# Query Parameter Learning start ----------
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#   return fake_items_db[skip : skip + limit]

# @app.get("/items/{item_id}")
# async def read_item2(item_id: str, q: str | None = None):
#   if q:
#     return {"item_id": item_id, "q": q}
#   return {"item_id": item_id}

# @app.get("/items/{item_id}")
# async def read_item_new(item_id: str, q: str | None = None, short: bool = False):
#   # breakpoint()
#   item = {"item_id": item_id}
#   if q:
#       item.update({"q": q})
#   if not short:
#       item.update(
#           {"description": "This is an amazing item that has a long description"}
#       )
#   return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
  user_id: int, item_id: str, q: str | None = None, short: bool = False
):
  item = {"item_id": item_id, "owner_id": user_id}
  if q:
      item.update({"q": q})
  if not short:
      item.update(
          {"description": "This is an amazing item that has a long description"}
      )
  return item

# @app.get("/items/{item_id}")
# async def read_user_item_test(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

@app.get("/items/{item_id}")
async def read_user_item_required_and_optional(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# Query Parameter Learning end ----------

# ************************************************************************

# Request body Learning start ----------
@app.post("/items/")
async def create_item(item: Item):
  item_dict = item.model_dump()
  if item.tax:
      price_with_tax = item.price + item.tax
      item_dict.update({"price_with_tax": price_with_tax})
  return item_dict

@app.put("/items/{item_id}")
async def create_item2(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@app.put("/itemsee/{item_id}")
async def create_item3(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# Request body Learning end ----------

# *********************************************************************

# Query Parameter And String Validation Learning start ----------
@app.get("/itemsqqq/")
async def read_items4(q: Annotated[str | None,
                                   Query(..., min_length=3)
                                         ]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# default value using Query...
@app.get("/itemsqqq/")
async def read_items4(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Query Parameter And String Validation Learning end ----------

# *****************************************************************

# Path Parameters and Numeric Validations Learning start ----------
@app.get("/itemseses/{item_id}")
async def read_items5(
  item_id: Annotated[int, Path(title="The ID of the item to get")],
  q: Annotated[str | None, Query(alias="item-query")] = None,
):
  results = {"item_id": item_id}
  if q:
      results.update({"q": q})
  return results

# Path Parameters and Numeric Validations Learning end ----------

# ******************************************************************

# Body - Multiple Parameters Learning start ----------
@app.put("/itemskkk/{item_id}")
async def update_item(item_id: int, item: Item, user: User,
                      importance: Annotated[int, Body(gt=0)],
                      q: str | None = None,):
  results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
  return results

# Body - Multiple Parameters Learning end ----------


# Body - Nested Models Learning start ----------
@app.post("/offers/")
async def create_offer(offer: Offer):
  return offer

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

# Body - Nested Models Learning end ----------

