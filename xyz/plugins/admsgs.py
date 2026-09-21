from pyrogram import Client as app, filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time, random
from asSQL import Client as cl
from .is_admin import admin, add_msg, owner

data = cl("protect")
db = data['data']

def rd(chat_id, text):
    rdodd = (db.get(f"group_{chat_id}_replies"))
    found = None
    info = None
    for i in rdodd:
        if f"{text}" in i:
            found = True
            info = i
        else:
            continue
    if found:
        return info
    else:
        return None

@app.on_message(filters.all & filters.group, group=33)
def handle_messages(app, message):
    chat_id = str(message.chat.id)
    text = message.text
    t = ((time.time()))
    if message.text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            if db.key_exists(f"user_{chat_id}_{message.from_user.id}_msgs") == 1:
                pass
            else:
                db.set(f"user_{chat_id}_{message.from_user.id}_msgs", [t])
        else:
            return
    if message.sender_chat:
        return
    add_msg(chat_id, message.from_user.id, 1)
    if (rd(message.chat.id, message.text)) != None:
        info = rd(message.chat.id, message.text)
        
        if info:
            if info[message.text]['type'] == "text":
                return message.reply(f"{info[message.text]['reply']}")
            else:
                file = info[message.text]['file']
                caption = info[message.text]['caption'] if info[message.text]['caption'] else "،"
                if caption and file:
                    app.send_cached_media(message.chat.id, file, caption=caption, reply_to_message_id=message.id)
    
    if db.get(f"running_rolet_{message.chat.id}"):
        info = db.get(f"running_rolet_info_{message.chat.id}")
        current_time = time.time()
        elapsed_time = current_time - float(info)
    
        if elapsed_time >= 300:
            db.delete(f"running_rolet_{message.chat.id}")
            db.delete(f"running_rolet_players_{message.chat.id}")
            db.delete(f"running_rolet_admin_{message.chat.id}")
            db.delete(f"running_rolet_info_{message.chat.id}")
            return app.send_message(chat_id=chat_id, text="شكله فيه روليت شغال ليها أكثر من 5 دقائق.. مسحتها :) ")

    name = "".join(random.choice(db.get('botname')))
    name2 = "عهد"
    
    bot_r = [
        f"اسمي {name}", "اسكت علينا", "مش بوته!", "طير من هنا", "الجو معبي", "الله يعين", "يا صبر الأرض", "نعمين", name2, "؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟", "يا راجل أزعجتنا", "الله يصبرني"
    ]
    
    bot_name = [
        "عيونها", "أهلين",
        "نعم", "تفضل يا عيوني", "عيوني ليك", "قول شنو عندك", "تفضل", "تأمرني",
        "مرحبتين والله", "شنو يا عمري",
        "نعمين", "روحها", "هاه",
        "زفت",
        f"الله يسامح {name}", "عيوني ليك", "نعم ", f"الله يعطيك عيشة غير {name} ",
        "تواصل مع مدير أعملي", "تفضل عيوني ليك",
        "عيوني", "؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟"
    ]
    
    sb = [
        "عيب عليك", "عيب", "يا طير عيب", "يا قليل التربية", "تحشم على وجهك", "؟؟؟؟؟؟", "يا ليت تتأدب", "نقص لسانك", "حاضر", " يا راجل عيب", "؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟", "أستغفر الله"
    ]
    
    lovem = [
        "سلمها يا ربي",
        "أكثر منك",
        "يا عمري أنت",
        "نعشقك",
        "بدينا في الكذب",
        "أحلى من يحبني",
        "يا سعدي والله",
        "أكثر أكثر أكثرر",
        "يا روحي",
        "نموت فيك"
    ]
    
    zg = [
        "عيب عليك", "عيب", "ضم فمك", "يا قليل التربية", "تحشم على وجهك", "؟؟؟؟؟؟", "يا ليت تتأدب", "نقص لسانك", "حاضر", "يا راجل عيب", "؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟ المخ"
    ]
    
    mm = [
        "أبركها من ساعة", "نحبك", "أكثر", "أزعجتنا يا راجل", "أمشي من هنا", "بااهي", "مش أكثر مني", "وبعدين؟", "جت منك", "توكل على الله بس"
    ]

    if text in db.get('bad_words'):
        return message.reply(random.choice(sb))
    if text == 'بوت':
        message.reply(random.choice(bot_r))
   
    if text == name2:
        message.reply(random.choice(bot_name))
   
    if text == 'احبك' or text == "احبج":
        message.reply(random.choice(lovem))
   
    if text == 'اكرهك':
        message.reply(random.choice(mm))
   
    if text == 'كليزق' or text == 'كلزق':
        message.reply(random.choice(zg))
