from peewee import Model, FloatField, CharField, ForeignKeyField, DatabaseProxy

proxy = DatabaseProxy()

class BaseModel(Model):
  class Meta:
    database = proxy

class User(BaseModel):
  username = CharField(unique=True)

class Group(BaseModel):
  chat_id = CharField(unique=True)
  
class GroupMember(BaseModel):
  group_id = ForeignKeyField(Group, backref="members")
  user_id = ForeignKeyField(User, backref="members")

class Debt(BaseModel):
  debtor_id = ForeignKeyField(GroupMember, backref='debt')
  creditor_id = ForeignKeyField(GroupMember, backref='debt')
  delta = FloatField()



