from peewee import Model, FloatField, CharField, ForeignKeyField, DatabaseProxy

proxy = DatabaseProxy()

class BaseModel(Model):
  class Meta:
    database = proxy

class User(BaseModel):
  username = CharField(
      unique=True, 
      verbose_name="Имя пользователя."
  )

  class Meta:
    verbose_name = "Пользователь" 
    verbose_name_plural = "Пользователи"

class Group(BaseModel):
  chat_id = CharField(
        unique=True,
        verbose_name="id чата"
  )
  class Meta:
    verbose_name = "Чат" 
    verbose_name_plural = "Чаты"
  
class GroupMember(BaseModel):
  group_id = ForeignKeyField(
        Group,
        backref="members",
        verbose_name="Чат участника."
  )
  user_id = ForeignKeyField(
        User,
        backref="members",
        verbose_name="Участник."
  )

  class Meta:
    verbose_name = "Участник группы." 
    verbose_name_plural = "Участники группы."

class Debt(BaseModel):
  debtor_id = ForeignKeyField(
        GroupMember,
        backref='debt',
        verbose_name="Должник."
  )
  creditor_id = ForeignKeyField(
        GroupMember,
        backref='debt',
        verbose_name="Давший в долг."
  )
  delta = FloatField(
        verbose_name="Оставшийся долг(мб отрицательный)."
  )

  class Meta:
    verbose_name = "Долг." 
    verbose_name_plural = "Должники."



