
from service.bot import Bot
import os

import time
import sys

webex_token = os.environ.get('webex_token')




if __name__ == '__main__':
    bot = Bot()
    bot.run_bot(webex_token)
    
    # Programar el reinicio del bot cada 12 horas.
    #schedule.every(12).hours.do(restart_bot, bot)


