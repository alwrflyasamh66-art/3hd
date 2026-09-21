From pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data'] 
@app.on_message(filters.text & filters.group)
def handle_messages(app, message):
    message.text = message.text
    chat_id = message.chat.id
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    
    if message.sender_chat:
        return
    if message.text == "إلغاء" or message.text == "الغاء" and db.get(f"add_rule_group_{chat_id}_{message.from_user.id}") == "pen" or message.text == "الغاء" and db.get(f"pending_{message.from_user.id}_{message.chat.id}_addw") == "pen" or message.text == "الغاء" and db.get(f"pending_{message.from_user.id}_{message.chat.id}_addcommand2") or message.text == "الغاء" and db.get(f"pending_{message.from_user.id}_{message.chat.id}_addcommand") or message.text == "الغاء" and db.get(f"pending_{chat_id}_delete_{message.from_user.id}") or message.text == "الغاء" and db.get(f"set_flood_{chat_id}_{message.from_user.id}") or message.text == "الغاء" and db.get(f"new_reply_{message.chat.id}_{message.from_user.id}") or message.text == "الغاء" and db.get(f"add_reply_{message.chat.id}_{message.from_user.id}") or message.text== "الغاء" and db.get(f"delete_reply_{message.chat.id}_{message.from_user.id}"):
        db.delete(f"add_rule_group_{chat_id}_{message.from_user.id}")
        db.delete(f"pending_{message.from_user.id}_{message.chat.id}_addw")
        db.delete(f"pending_{message.from_user.id}_{message.chat.id}_addcommand2")
        db.delete(f"pending_{message.from_user.id}_{message.chat.id}_addcommand")
        db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
        db.delete(f"add_reply_{message.chat.id}_{message.from_user.id}")
        db.delete(f"pending_{chat_id}_delete_{message.from_user.id}")
        db.delete(f"delete_reply_{message.chat.id}_{message.from_user.id}")
        db.delete(f"set_flood_{chat_id}_{message.from_user.id}")
        message.reply(f'⇜ تم، ألغيت الأمر')
        return
    if db.get(f"new_reply_{message.chat.id}_{message.from_user.id}"):
       
        if message.text:
            old = db.get(f"group_{message.chat.id}_replies")
            rd = db.get(f"new_reply_{message.chat.id}_{message.from_user.id}")
            d = {f"{rd}":{"by":message.from_user.id,"date":f"{message.date}","reply":message.text,"type":"text"}}
            old.append(d)
            db.set(f"group_{message.chat.id}_replies",old)
            db.delete(f"new_reply_{message.chat.id}_{message.from_user.id}")
            return message.reply(f"الرد {rd} انضاف.")
    if db.get(f"delete_reply_{message.chat.id}_{message.from_user.id}"):
        rd = message.text
        rdod = db.get(f"group_{message.chat.id}_replies")
        found = False
        for i in rdod:
            if f"{rd}" in i:
                rdod.remove(i)
                found = True
            else:
                pass
        if found:
            db.set(f"group_{message.chat.id}_replies",rdod)
            db.delete(f"delete_reply_{message.chat.id}_{message.from_user.id}")
            return message.reply(f"الرد {rd} انمسح.")
        else:
            db.delete(f"delete_reply_{message.chat.id}_{message.from_user.id}")
            return message.reply(f"ملقيتش {rd}")
    if db.get(f"add_reply_{message.chat.id}_{message.from_user.id}"):
        word = message.text
        db.delete(f"add_reply_{message.chat.id}_{message.from_user.id}")
        db.set(f"new_reply_{message.chat.id}_{message.from_user.id}",word)
        return message.reply(f"توا ابعت الرد:\n( نص، صورة، فيديو، متحركة، بصمة، أغنية ) ")
    if db.get(f"set_flood_{chat_id}_{message.from_user.id}"):
        num = None
        try:
            num = int(message.text)
        except:
            db.delete(f"set_flood_{chat_id}_{message.from_user.id}")
            return message.reply("لازم يكون رقم!")
        if num < 0:
            db.delete(f"set_flood_{chat_id}_{message.from_user.id}")
            return message.reply("ملاحظ أن الرقم صغير هلبا؟")
        if num > 14:
            db.delete(f"set_flood_{chat_id}_{message.from_user.id}")
            return message.reply("لازم يكون أقل من 14")
        else:
            db.set(f"group_{message.chat.id}_flood",message.text)
            db.delete(f"set_flood_{chat_id}_{message.from_user.id}")
            return message.reply(f"تم، حددت {message.text} كـ رقم للفلود.")
    if db.get(f"pending_{chat_id}_delete_{message.from_user.id}"):
        c = db.key_exists(f"group_{message.chat.id}_custom_{message.text}")
        if c == 1:
            db.delete(f"pending_{chat_id}_delete_{message.from_user.id}")
            db.delete(f"group_{message.chat.id}_custom_{message.text}")
            return message.reply("⇜ تم، مسحت الأمر.")
        else:
            db.delete(f"pending_{chat_id}_delete_{message.from_user.id}")
            return message.reply("ما فيش أمر بالطريقة هادي!")
    if db.get(f'pending_{message.from_user.id}_{message.chat.id}_addcommand') == "pen":
        db.set(f'pending_{message.from_user.id}_{message.chat.id}_addcommand2',"pen")
        db.delete(f'pending_{message.from_user.id}_{message.chat.id}_addcommand')
        db.set(f'pending_{message.from_user.id}_{message.chat.id}_addcommand_old',f"{message.text}")
        return message.reply('⇜ تم، توا ابعت الأمر الجديد')
    if db.get(f'pending_{message.from_user.id}_{message.chat.id}_addcommand2'):
        old_cmd = db.get(f'pending_{message.from_user.id}_{message.chat.id}_addcommand_old')
        new = message.text
        if old_cmd == new:
            db.delete(f'pending_{message.from_user.id}_{message.chat.id}_addcommand_old')
            db.delete(f'pending_{message.from_user.id}_{message.chat.id}_addcommand2')
            return message.reply("⇜ الأمر موجود أو كيفه بالضبط!")
        else:
            db.set(f"group_{message.chat.id}_custom_{new}",f"{old_cmd}")
            db.delete(f'pending_{message.from_user.id}_{message.chat.id}_addcommand_old')
            db.delete(f'pending_{message.from_user.id}_{message.chat.id}_addcommand2')
            return message.reply("⇜ تم، ضفت الأمر الجديد.")
        
    if db.get(f"pending_{message.from_user.id}_{message.chat.id}_addw") == "pen":
        db.set(f"group_{message.chat.id}_welcome",message.text)
        db.delete(f"pending_{message.from_user.id}_{message.chat.id}_addw")
        return message.reply("⇜ تم، حددت الترحيب الجديد.")
    if db.get(f"add_rule_group_{chat_id}_{message.from_user.id}") == "pen":
        db.set(f"group_{message.chat.id}_rules",message.text)
        db.delete(f"add_rule_group_{chat_id}_{message.from_user.id}")
        return message.reply("⇜ تم، حددت القوانين الجديدة.")
    if message.text == "اضف قوانين" or message.text == "تعيين قوانين" or message.text == "تعين قوانين":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"add_rule_group_{chat_id}_{message.from_user.id}","pen")
            return message.reply("⇜ توا ابعت القانون الجديد.")
    if message.text  == "تعيين ترحيب" or message.text == "اضف ترحيب":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"pending_{message.from_user.id}_{message.chat.id}_addw","pen")
            return message.reply("↢ توا ابعت الترحيب الجديد..")
        else:
            return message.reply("↢ الأمر هذا للـ ( المالك ، الأدمن ) بس")
    if message.text == "اضف امر":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"pending_{message.from_user.id}_{message.chat.id}_addcommand","pen")
            return message.reply("↢ توا ابعت الأمر القديم..")
    if message.text == "حذف امر":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"pending_{chat_id}_delete_{message.from_user.id}",True)
            return message.reply("↢ توا ابعت الأمر..")
    if message.text == "تعيين تكرار" or message.text == "تعين تكرار":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"set_flood_{chat_id}_{message.from_user.id}",True)
            return message.reply("↢ توا ابعت رقم التكرار (لازم رقم، وأقل من 14 )..")
    if message.text == "اضف رد":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"add_reply_{message.chat.id}_{message.from_user.id}",True)
            return message.reply("↢ توا ابعت الكلمة..")
        else:
            return message.reply("↢ الأمر هذا للـ ( المالك ، الأدمن ) بس")
    if message.text == "حذف رد":
        if owner(message.from_user.id,message.chat.id) or admin(message.from_user.id,message.chat.id):
            db.set(f"delete_reply_{message.chat.id}_{message.from_user.id}",True)
            return message.reply("↢ توا ابعت الرد..")
        else:
            return message.reply("↢ الأمر هذا للـ ( المالك ، الأدمن ) بس")
