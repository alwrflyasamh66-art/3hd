from pyrogram import Client
from pyrogram import  filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl


data = cl("protect")
db = data['data']
db.create_table()
db.set("botname",['ميرا' , 'ميرال' , 'بوت' ,'ميروو' , 'ميرا'])
db.set("bad_words",['كس','عير','طيز','زب','كسمك','كسختك','طيزك','مص'])

plugins = dict(root="plugins")

Client("x",
api_id=39978956,
api_hash="e7322ed176f1527600979186b4ea8da8",
bot_token="8854898075:AAEySMV38C1Znqagp7VinKJiaNP3H_mp_NE", plugins=plugins).run()
