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
  group_id = ForeignKeyField(group_ids, backref="members")
  user_id = ForeignKeyField(user_ids, backref="members")

class debts(BaseModel):
  debt_id = IntegerField(unique=True)
  chat_id = ForeignKeyField(group_ids, backref='debt')
  debtor_id = ForeignKeyField(group_members, backref='debt')
  creditor_id = ForeignKeyField(group_members, backref='debt')



