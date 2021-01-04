from typing import List, Optional
from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [{"item_name": "Foo1"}, {"item_name": "Bar2"}, {"item_name": "Baz3"}, {"item_name": "Hay4"}]


@app.get("/")
@app.get("/hello_world")
async def hello_world():
    """Hello world endpoint for testing if FastAPI works properly"""
    return {"message": "Hello World, E!"}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """Accepting query parameters"""
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    """Items endpoint for testing path parameters with optional query parameters"""
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    else:
        item.update(
            {"description": "short description"}
        )
    return item


@app.get("/users/me")
async def read_user_me():
    """Path order matters. '/users/me' should come first and '/users/{user_id}' can come only after that"""
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    """Path order matters. '/users/me' should come first and '/users/{user_id}' can come only after that"""
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """Path with predefined values"""
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """Path parameters containing paths"""
    return {"file_path": file_path}


@app.get("/users_multi/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    """Multiple path and query parameters"""
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.post("/items/")
async def create_item(item: Item):
    """Accepting data in the request body for a POST endpoint"""
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    """Request body + path + query parameters"""
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#
# Query Parameters and String Validations
#


@app.get("/itemsv2/")
# Default value and regular expressions:
# async def read_items(q: Optional[str] = Query("fixedquery", min_length=3, max_length=50, regex="^fixedquery$")):
# No default value, but 'q' is a required parameter:
async def read_items(q: Optional[str] = Query(..., min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query parameter list / multiple values
@app.get("/itemsv3/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items


# Query parameter list / multiple values with defaults
@app.get("/itemsv4/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# Declare more metadata
@app.get("/itemsv5/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Alias parameters
@app.get("/itemsv6/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecating parameters
@app.get("/itemsv7/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
