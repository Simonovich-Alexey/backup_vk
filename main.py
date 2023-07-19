import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN_YD')
DOMAIN = os.getenv('DOMAIN')

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
    print(TOKEN)
    print(DOMAIN)
