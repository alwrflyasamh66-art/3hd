from pyrogram import Client
from pyrogram import  filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl


data = cl("protect")
db = data['data']
db.create_table()
db.set("botname",['عهد' , 'عهود' , 'بوت' ,'عاهد' , 'عهو'])
db.set("bad_words",['كس','عير','طيز','زب','كسمك','كسختك','طيزك','مص'])

plugins = dict(root="plugins")

Client("x",
api_id=37339435,
api_hash="c701d54aa378e57434d46d74f8b75f9c",
bot_token="8566481559:AAHktUpD5KtzpgG_mMGBPQ3qCucImDeDm-I", plugins=plugins).run()