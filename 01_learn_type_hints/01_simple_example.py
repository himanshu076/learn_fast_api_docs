from datetime import datetime
from pydantic import BaseModel
from typing import Annotated


def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + f"{age}"
    return name_with_age

def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_e

def process_items(items: list[str]):
    for item in items:
        print(item)

def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s

def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)

def process_item(item: int | str):
    """here can declair may tyoe of the variable seperated by | new in python 3.10"""
    print(item)

def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

class Person:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: Person):
    return one_person.name


class User(BaseModel):
    id: int
    name: str = "Jhon Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

user = User(**external_data)


def say_hello(name: Annotated[str, "this is just metadata"]) -> Annotated[str, "Area of the string rectangle in square meters"]:
    return f"Hello {name}"


if __name__ == "__main__":
  print(get_full_name("john/", "doe"))
  print(get_name_with_age("ggggg", 23))
  print(user)
  print(user.id, user.friends)
  print(say_hello.__annotations__)
