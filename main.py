from db.__init__ import __init__ 
import logic.services as lss

def main() -> None :
    __init__()
    user1 = '@denisbulgakow'
    user2 = '@egor_zarubin'
    user3 = '@ArtemS_31'
    lss.add_user(user1)
    lss.add_user(user2)
#PYTHONPATH=src:src/db:src/logic python main.py
    print(lss.get_user_id(user1))
    print(lss.get_user_id(user2))
    print(lss.get_user_id(user3))



if __name__ == '__main__':
    main()
