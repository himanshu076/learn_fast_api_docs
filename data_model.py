from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
  url: HttpUrl
  name: str


class Item(BaseModel):
  name: str
  description: str | None = None
  price: float
  tax: float | None = None
  # tags: list = []
  # tags2: list[str] = []
  # tags2: set[str] = set()
  # image: list[Image] | None = None

  # Extra JSON Schema data in Pydantic models
  model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

# class Item(BaseModel):
#   name: str
#   description: str | None = Field(
#       default=None, title="The description of the item", max_length=300, , examples=["A very nice Item"]
#   )
#   price: float = Field(gt=0, description="The price must be greater than zero", examples=[35.4])
#   tax: float | None = Field(default=None, examples=[3.2])

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
  username: str
  full_name: str | None = None
