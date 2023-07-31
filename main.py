import os
from dotenv import load_dotenv
import modules.YaUploader as YaUploader
from modules.VKClient import get_token_vk


if __name__ == '__main__':
    load_dotenv()
    TOKEN_YD = os.getenv('TOKEN_YD')
    TOKEN_VK = os.getenv('TOKEN_VK')
    USER_ID = os.getenv('USER_ID')

    user_one = YaUploader.YaUploader(TOKEN_VK, USER_ID, TOKEN_YD, 30)
    # get_token_vk()

