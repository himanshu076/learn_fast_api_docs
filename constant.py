from enum import Enum

class ModelName(str, Enum):
  alexnet = 'alexnet'
  resnet = 'resnet'
  lenet = 'lenet'


class Tags(Enum):
  """use it in method to create sapration of apis """
  items = 'items'
  users = 'users'