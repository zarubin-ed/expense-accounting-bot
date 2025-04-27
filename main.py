from db.__init__ import __init__ 
from handlers.run_bot import run_bot
from logic.services import *

def main() -> None : #PYTHONPATH=src python main.py
    __init__()
    run_bot()
    
if __name__ == '__main__':
    main()