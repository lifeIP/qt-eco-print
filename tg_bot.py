from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from time import time

from werkzeug.utils import secure_filename

import asyncio
import logging

from manage_service_data import get_service_data_from_file, set_service_data_into_file

BOT_TOKEN = "6127190393:AAHTTLBdq1x9bt6NUFgJetvMdljQf_tCnOE"
ALLOWED_EXTENSIONS = set(['pdf'])

class Session:
    def __init__(self):
        self.m_chat_id:str = ""
        self.session_ID:str = ""

    def init_new_session(self, session_ID:str, chat_ID:str):
        app_status = get_service_data_from_file("app_status")
        if app_status is None:
            return -1
        
        if app_status == "busy":
            return -1
        
        if app_status == "free":
            if session_ID != get_service_data_from_file("session_id"): return -1
            set_service_data_into_file("chat_id", str(chat_ID))
            
            self.session_ID = session_ID
            self.m_chat_id = chat_ID
            # set_service_data_into_file("app_status", "busy")
            # set_service_data_into_file("bot_request", "newuser")
            return 1
        return -1
    
    def set_file_path(self, path:str, chat_ID:str):
        if chat_ID == self.m_chat_id:
            if get_service_data_from_file("app_status") == "busy":
                return 0
            set_service_data_into_file("file_path", path)
            set_service_data_into_file("bot_request", "path")
            return 1
        return -1


        

client_part = Session()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

router = Router()


@router.message(F.document)
async def get_doc(message: types.Message):
    path = secure_filename(message.document.file_name)

    if allowed_file(message.document.file_name):
        await message.bot.download(message.document, destination= "documents/" + path)
        stat = client_part.set_file_path(path=path, chat_ID=str(message.chat.id))
        if stat == -1:
            await message.answer("В данный момент принтер занят")
            return
        elif stat == 0:
            await message.answer("Ваш файл получен. Для того, чтобы изменить файл, перейдите на главную страницу и отсканируйте qr-код заново.")
            return    
        await message.answer("Ваш файл получен. Обратите внимание на экран аппарата.")
    else:
        await message.answer("Ваш файл не подходит под условия(pdf)")



dp = Dispatcher()
dp.include_routers(router)


@dp.message(Command('start'))
async def handle_start(message: types.Message):
    if client_part.init_new_session(session_ID=message.text[7:], chat_ID=str(message.chat.id)) == -1:
        await message.answer("Привет! Спасибо что пользуешься нашими услугами🙂") 
        await message.answer("В данный момент принтер занят")
    else:
        await message.answer("Привет! Спасибо что пользуешься нашими услугами🙂") 
        await message.answer("Адрес: г.Томск ул.Кирова д.56а")
        await message.answer("Отправьте файл для печати. Это может быть pdf")



async def bot_main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


def bot_start():
    asyncio.run(bot_main())
