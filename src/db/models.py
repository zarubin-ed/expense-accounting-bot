#from db.__init__ import db
from peewee import Model, IntegerField, CharField, ForeignKeyField, DatabaseProxy

proxy = DatabaseProxy()

class BaseModel(Model):
  class Meta:
    database = proxy

class user_ids(BaseModel):
  user_id = IntegerField(unique=True)
  username = CharField()

class group_ids(BaseModel):
  group_id = IntegerField(unique=True)
  chat_id = CharField()
  
class group_members(BaseModel):
  member_id = IntegerField(unique=True)
  chat_id = CharField()
  user_id = IntegerField()

class debts(BaseModel):
  debt_id = IntegerField(unique=True)
  chat_id = CharField()
  debtor_id = IntegerField()
  creditor_id = IntegerField()



