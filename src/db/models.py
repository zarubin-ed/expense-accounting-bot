from peewee import Model, IntegerField, CharField, ForeignKeyField, DatabaseProxy

proxy = DatabaseProxy()

class BaseModel(Model):
  class Meta:
    database = proxy

class UserIds(BaseModel):
  username = CharField(unique=True)

class GroupIds(BaseModel):
  chat_id = CharField(unique=True)
  
class GroupMembers(BaseModel):
  group_id = ForeignKeyField(GroupIds, backref="members")
  user_id = ForeignKeyField(GroupIds, backref="members")

class Debts(BaseModel):
  debtor_id = ForeignKeyField(GroupMembers, backref='debt')
  creditor_id = ForeignKeyField(GroupMembers, backref='debt')
  delta = IntegerField()



