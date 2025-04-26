from db.__init__ import __init__ 
import logic.services as lss

def main() -> None :
    __init__()
    lss.add_user(888, "имя")
    lss.add_user(888, "имя")

if __name__ == '__main__':
    main()
