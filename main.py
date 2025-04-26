from db.__init__ import __init__ 
from logic.services import *

def main() -> None :
    __init__()
    user1 = '@denisbulgakow'
    user2 = '@egor_zarubin'
    user3 = '@ArtemS_31'

    chat1 = 'id=888'
    chat2 = 'id=88'

    print(whom_does_this_user_owe(user1, chat1))
    print(whom_does_this_user_owe(user2, chat1))

    register_debt(user1, user2, chat2, 100)

    print(whom_does_this_user_owe(user1, chat1))
    print(whom_does_this_user_owe(user2, chat1))

    register_debt(user1, user2, chat1, 100)

    print(whom_does_this_user_owe(user1, chat1))
    print(whom_does_this_user_owe(user2, chat1))

    register_debt_free(user1, user2, chat1, 100)

    print(whom_does_this_user_owe(user1, chat1))
    print(whom_does_this_user_owe(user2, chat1))
   
#PYTHONPATH=src:src/db:src/logic python main.py




if __name__ == '__main__':
    main()
