from pyrogram import Client as app, filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions
import time
from asSQL import Client as cl
from .is_admin import admin, add_msg, owner

data = cl("protect")
db = data['data']

# القناة المطلوبة للاشتراك الإجباري
MUST_JOIN = "a990099aa"

def rank_is(user_id, chat_id):
    if user_id in db.get(f"admins-{chat_id}"):
        return "الأدمن"
    if user_id in db.get(f"creators_{chat_id}"):
        return "المالك"
    else:
        return "عضو"

@app.on_message(filters.text & filters.group, group=32)
def handle_messages(app, message):
    chat_id = str(message.chat.id)
    text = message.text

    # --- بداية كود الاشتراك الإجباري ---
    if message.from_user:
        try:
            user_status = app.get_chat_member(MUST_JOIN, message.from_user.id)
            if user_status.status in [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]:
                return message.reply(
                    f"يا غالي لازم تشترك في القناة الأولى عشان تقدر تستخدم البوت:\nhttps://t.me/{MUST_JOIN}",
                    disable_web_page_preview=True
                )
        except Exception:
            return message.reply(
                f"يا غالي لازم تشترك في القناة الأولى عشان تقدر تستخدم البوت:\nhttps://t.me/{MUST_JOIN}",
                disable_web_page_preview=True
            )
    # --- نهاية كود الاشتراك الإجباري ---

    if text:
        if db.key_exists(f'group_{message.chat.id}') == 1:
            pass
        else:
            return
    if message.sender_chat:
        return
    
    if db.get(f"group_{message.chat.id}_custom_{text}"):
        text = db.get(f"group_{message.chat.id}_custom_{text}")

    if text == "تنزيل الكل":
        if owner(message.from_user.id, message.chat.id):
            ad = db.get(f"admins-{message.chat.id}")
            if len(ad) == 1:
                return message.reply("⇜ مافيش أدمنية ولا رتب توا.")
            for ix in ad:
                db.unpush(f"admins-{message.chat.id}", ix)
            inf = f"""
    ⇜ مرحبتين بيك يا مالك يا أساسي
    ⇜ نزلّت ( {len(ad)} ) من الأدمنية.
    
    ༄
            """
            return message.reply(inf)

    if text == "المالكين" or text == "مالكين" or text == "مالك":
        admin_list = db.get(f"creators_{message.chat.id}")
        
        if len(admin_list) <= 0:
            return message.reply("⇜ مافيش مالكين.")
        admin_string = "المالكين :\n"
        s = 0
        for admin_id in (admin_list):
            try:
                user = app.get_chat_member(message.chat.id, admin_id)
                username = user.user.username if user.user.username is not None else ""
                s += 1
            except Exception as e:
                s += 1
                admin_string += f"{s} - @ ⇜ (<code>{admin_id}</code>)\n"
                continue

            admin_string += f"{s} - @{username} ⇜ (<code>{admin_id}</code>)\n"

        enums.ParseMode.DEFAULT
        return message.reply(admin_string)

    if text == "الادمنيه" or text == "الادمنية" or text == "ادمنيه":
        print(db.get(f"admins-{message.chat.id}"))
        admin_list = db.get(f"admins-{message.chat.id}")
        if len(admin_list) < 1:
            return message.reply("⇜ مافيش أدمنية.")
        admin_string = "الأدمنية :\n"
        s = 0
        for admin_id in (admin_list):
            try:
                user = app.get_chat_member(message.chat.id, admin_id)
                username = user.user.username if user.user.username is not None else ""
                s += 1
            except Exception as e:
                s += 1
                admin_string += f"{s} - @ ⇜ (<code>{admin_id}</code>)\n"
                continue

            admin_string += f"{s} - @{username} ⇜ (<code>{admin_id}</code>)\n"

        enums.ParseMode.DEFAULT
        return message.reply(admin_string)

    if text == "معلومات الكروب" or text == "معلوماتنا" or text == "الاعدادات":

        lock_status = {
                'stickers': None,
                'flood': None,
                'badword': None,
                "edit": None,
                "id": None,
                "yt": None,
                'bigmsg': None,
                'text': None,
                'forwards': None,
                'inline': None,
                'gifs': None,
                'contact': None,
                'documents': None,
                'photos': None
            }

        for type, status in lock_status.items():
            lock_status[type] = db.get(f'lock_{type}_{chat_id}')

        output = "قائمة القفل والفتح :\n"
        for type, status in lock_status.items():
            output += f"{type} ⇜ {'مقفول' if status else 'مفتوح'}\n"

        return message.reply(
            output.replace("stickers", 'الملصقات').replace(
                "text", 'الدردشة').replace('flood', 'التكرار').replace("gifs", 'المتحركات').replace(
                    "documents",
                    'الملفات').replace("forwards", 'التوجيهات').replace(
                        "contact", 'جهة اتصال').replace("photos", 'الصور').replace("badword", 'السب').replace("id", 'الأيدي').replace("inline", 'الإشعارات').replace("edit", 'التعديل').replace('bigmsg', 'الكلايش').replace('yt', 'يوتيوب'))

    if text.startswith("فك تقييد"):
        import re
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5836188784:
                    return message.reply("خير إن شاء الله؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.restrict_chat_member(chat_id, target, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
                return message.reply(f"""
    ⇜ الفرخ 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم فك تقييده.
    ༄
                """)
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")

    if text.startswith("تقييد"):
        import re
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5836188784:
                    return message.reply("خير إن شاء الله؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.restrict_chat_member(chat_id, target, ChatPermissions())
                return message.reply(f"""
    ⇜ الفرخ 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ تم تقييده.
    ༄
                """)
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")

    if text.startswith("تنظيف "):
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            count = int(text.split(" ")[1])
            if count > 400:
                message.reply("⇜ لازم أقل من 400 يا طير")
            else:
                for msg in range(message.id, message.id - count, -1):
                    try:
                        app.delete_messages(message.chat.id, msg)
                    except:
                        continue
                app.send_message(message.chat.id, f"تم مسح ⇜ {count}")
                return

    if text == "المكتومين" or text == "مكتومين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            my_dict = db.get(f"group_{chat_id}_mutelist")
            if len(my_dict['data']) < 1:
                return message.reply("⇜ مافيش مكتومين.")
            
            counter = 1
            mtot = "المكتومين :\n"
            for d in my_dict['data']:
                for key, value in d.items():
                    if counter > 100:
                        return message.reply(mtot)
                        break
                    else:
                        m1 = (f"{counter} - (`{key}`) [**{value['name']}**] \n")
                        mtot += m1 + "\n"
                        counter += 1
            
            return message.reply(mtot)

    if text == "محظورين" or text == "المحظورين" or text == "المحظوريين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED)
           
            response = "المحظورين : \n"
            count = 1

            for muted_user in muted_users:
                if count > 100:
                    response += "\n⇜ البوت يدير في سكب للحسابات المحذوفة.\n࿓"
                    return message.reply(response, parse_mode=enums.ParseMode.HTML)
                    
                if muted_user.user.is_deleted == True:
                    continue
                else:
                    username = f"@{muted_user.user.username}" if muted_user.user.username else f"[{muted_user.user.mention}]"
                    response += f"{count} ⇜ {username} ࿓ ( <code>{muted_user.user.id}</code> ) \n".replace("Deleted Account", "0")
                    count += 1
            if count == 1:
                return message.reply("⇜ مافيش محظورين.")
            else:
                response += "\n⇜ البوت يدير في سكب للحسابات المحذوفة.\n࿓"
                return message.reply(response, parse_mode=enums.ParseMode.HTML)

    if text == "مقيدين" or text == "المقيدين" or text == "المقيديين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED)
           
            response = "المقيدين : \n"
            count = 1

            for muted_user in muted_users:
                if count > 100:
                    response += "\n⇜ البوت يدير في سكب للحسابات المحذوفة.\n࿓"
                    return message.reply(response, parse_mode=enums.ParseMode.HTML)
                    break
                if muted_user.user.is_deleted == True:
                    continue
                if muted_user.permissions.can_send_messages == True:
                    continue
                else:
                    username = f"@{muted_user.user.username}" if muted_user.user.username else f"[{muted_user.user.mention}]"
                    response += f"{count} ⇜ {username} ࿓ ( <code>{muted_user.user.id}</code> ) \n".replace("Deleted Account", "0")
                    count += 1
            if count == 1:
                return message.reply("⇜ مافيش مقيدين.")
            else:
                response += "\n⇜ البوت يدير في سكب للحسابات المحذوفة.\n࿓"
                return message.reply(response, parse_mode=enums.ParseMode.HTML)

    if text == "مسح لمحظورين" or text == "مسح محظورين" or text == "مسح المحظورين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED)
           
            count = 1

            for muted_user in muted_users:
                app.unban_chat_member(chat_id, muted_user.user.id)
                count += 1
            if count == 1:
                message.reply("↢ مافيش محظورين.")
            else:
                message.reply(f"↢ مرحبتين يا {rank_is(message.from_user.id,message.chat.id)}، مسحت {count} محظور.")
                return

    if text == "مسح لمقيدين" or text == "مسح مقيدين" or text == "مسح المقيدين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            muted_users = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED)
           
            count = 1

            for muted_user in muted_users:
                if muted_user.permissions.can_send_messages == True:
                    continue
                else:
                    app.restrict_chat_member(chat_id, muted_user.user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
                    count += 1
            if count == 1:
                message.reply("↢ مافيش مقيدين.")
            else:
                message.reply(f"↢ مرحبتين يا {rank_is(message.from_user.id,message.chat.id)}، مسحت {count} مقيد.")
                return

    if text == "رفع ادمن" and message.reply_to_message:
        usr_id = message.reply_to_message.from_user.id
        if usr_id == 5836188784:
            return message.reply("خير إن شاء الله؟")
        if owner(message.from_user.id, message.chat.id):
            if admin(usr_id, message.chat.id):
                return message.reply(f"""
⇜ الفرخ هذا 「 {message.reply_to_message.from_user.mention}
⇜ أصلاً أدمن يا طير.
༄
            """)
            else:
                db.push(f"admins-{message.chat.id}", usr_id)
                return message.reply(f"""
⇜ الفرخ هذا 「 {message.reply_to_message.from_user.mention}
⇜ قعد أدمن توا!
༄
            """)
        else:
            return message.reply("الأمر يخص ( المالكين ) بس.")

    if text == "تنزيل ادمن" and message.reply_to_message:
        usr_id = message.reply_to_message.from_user.id
        if usr_id == 5836188784:
            return message.reply("خير إن شاء الله؟")
        if owner(message.from_user.id, message.chat.id):
            if admin(usr_id, message.chat.id):
                return message.reply(f"""
⇜ الفرخ هذا 「 {message.reply_to_message.from_user.mention}
⇜ أصلاً مش أدمن.
༄
            """)
            else:
                db.unpush(f"admins-{message.chat.id}", usr_id)
                return message.reply(f"""
⇜ الفرخ هذا 「 {message.reply_to_message.from_user.mention}
⇜ نزل التوا من الأدمنية!
༄
            """)
        else:
            return message.reply("الأمر يخص ( المالكين ) بس.")

    if text.startswith("كتم"):
        import re
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            target = None
            
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5836188784:
                    return message.reply("خير إن شاء الله؟")
                if (admin(target, message.chat.id) or owner(target, message.chat.id)):
                    return message.reply("يا راجل تقدرش تكتم الأدمنية ولا المالكين!")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    name = None
                    
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
                        name = app.get_users(username).first_name
            if target:
                ff = False
                users = db.get(f"group_{chat_id}_mutelist")
                for i in users['data']:
                    if f"{target}" in i:
                        ff = True
                    else:
                        continue
                if ff:
                    return message.reply(f"""
⇜ الفرخ 「 {name} 」 
⇜ مكتوم من قبل.
༄
            """)
                else:
                    try:
                        if str(target).isdigit():
                            if (admin(target, message.chat.id) or owner(target, message.chat.id)):
                                return message.reply("يا راجل تقدرش تكتم الأدمنية ولا المالكين!")
                            else:
                                name = app.get_chat_member(chat_id, target).user.first_name
                                username = app.get_chat_member(chat_id, target).user.username
                                new_mute = {target: {"name": name, "date": f"{message.date}", "username": f"{username}"}}
                                users['data'].append(new_mute)
                                print(users)
                                db.set(f"group_{chat_id}_mutelist", users)
                                return message.reply(f"""
            ⇜ الفرخ 「 {name} 」 
            ⇜ كتمته لك.
            ༄
                        """)
                        else:
                            name = app.get_users(target).user.first_name
                            mn = app.get_users(target).user.mention
                            username = app.get_users(target).user.username
                            new_mute = {target: {"name": name, "date": f"{message.date}", "username": f"{username}"}}
                            users['data'].append(new_mute)
                            print(users)
                            db.set(f"group_{chat_id}_mutelist", users)
                            return message.reply(f"""
        ⇜ الفرخ 「 {mn} 」 
        ⇜ كتمته لك.
        ༄
                    """)
                    except:
                        new_mute = {target: {"name": target, "date": f"{message.date}", "username": ""}}
                        users['data'].append(new_mute)
                        print(users)
                        db.set(f"group_{chat_id}_mutelist", users)
                        return message.reply(f"""
        ⇜ الفرخ 「 {app.get_users(target).user.mention} 」 
        ⇜ كتمته لك.
        ༄
                    """)
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")

    if text.startswith("فك كتم"):
        import re
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5836188784:
                    return message.reply("خير إن شاء الله؟")
                if (admin(target, message.chat.id) or owner(target, message.chat.id)):
                    return message.reply("يا راجل تقدرش تكتم الأدمنية ولا المالكين!")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
                        name = app.get_users(username).first_name
            if target:
                ff = False
                users = db.get(f"group_{chat_id}_mutelist")
                
                for i in users['data']:
                    if f"{target}" in i:
                        ff = True
                        users['data'].remove(i)
                        db.set(f"group_{chat_id}_mutelist", users)
                    else:
                        continue
                
                if ff:
                    if str(target).isdigit():
                        if (admin(target, message.chat.id) or owner(target, message.chat.id)):
                            return message.reply("يا راجل تقدرش تكتم الأدمنية ولا المالكين!")
                        else:
                            return message.reply(f"""
⇜ الفرخ 「 {app.get_chat_member(message.chat.id,target).user.mention} 」 
⇜ فكيت كتمه.
༄
            """)
                    else:
                        return message.reply(f"""
⇜ الفرخ 「 {app.get_users(target).user.first_name} 」 
⇜ فكيت كتمه.
༄
            """)
                else:
                    try:
                        if str(target).isdigit():
                            return message.reply(f"""
    ⇜ الشاب 「 {app.get_chat_member(message.chat.id,target).user.mention} 」 
    ⇜ مش مكتوم أصلاً.
    ༄
                    """)
                        else:
                            return message.reply(f"""
    ⇜ الشاب 「 {app.get_users(target).user.first_name} 」 
    ⇜ مش مكتوم أصلاً.
    ༄
                    """)
                    except:
                        return message.reply(f"""
    ⇜ الشاب 「 {target} 」 
    ⇜ مش مكتوم أصلاً.
    ༄
                    """)
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")

    if text == "مسح المكتومين":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            data = db.get(f"group_{chat_id}_mutelist")
            users = data['data']
            hm = len(users)
            if hm == 0: 
                return message.reply("⇜ مافيش مكتومين باش تمسحهم.")
            else:
                l = []
                db.set(f"group_{chat_id}_mutelist", {"data": l})
                return message.reply(f"⇜ تم، مسحت {hm} شخص مكتوم.")
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")

    if text == "الردود":
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            c = db.get(f"group_{chat_id}_replies")
            
            if len(c) == 1:
                return message.reply("⇜ مافيش ردود.")
            else:
                x = "⇜ الردود :\n"
                count = 1
                for item in c:
                    key = list(item.keys())[0]
                    try:
                        type = item[key]['type']
                        if type == 'text':
                            x += f'{count} ⇜ {key} | [{type}] \n'
                            count += 1
                        else:
                            x += f'{count} ⇜ {key} | [{type}] \n'
                            count += 1
                    except:
                        continue
                return message.reply(x.replace("animation", 'متحركة').replace("video", 'فيديو').replace("text", 'نص').replace("audio", 'أغنية').replace("voice", 'فويس').replace("photo", 'صورة').replace("document", 'ملف'))

    if text == "مسح الردود":
        if owner(message.from_user.id, message.chat.id):
            v = len(db.get(f"group_{chat_id}_replies"))
            db.set(f"group_{chat_id}_replies", [{"rd": False}])
            return message.reply(f"⇜ مسحت {v} رد.")
        else:
            return message.reply("⇜ الأمر هذا يخص ( المالك وفوق بس )")

    if text.startswith("طرد"):
        import re
        if owner(message.from_user.id, message.chat.id) or admin(message.from_user.id, message.chat.id):
            target = None
            reply_to_message = message.reply_to_message
            if reply_to_message:
                target = reply_to_message.from_user.id
                if target == 5836188784:
                    return message.reply("خير إن شاء الله؟")
            else:
                match = re.search(r"\d{9,}", text)
                if match:
                    target = int(match.group())
                else:
                    username = re.search(r"@[a-zA-Z0-9_]{5,}", text)
                    if username:
                        username = username.group()
                        target = app.get_users(username).id
            if target:
                app.ban_chat_member(message.chat.id, target)
                app.unban_chat_member(message.chat.id, target)
                return message.reply(f"""
    ⇜ الفرخ 「 {app.get_chat_member(chat_id,target).user.mention} 」 
    ⇜ طردته خارج المجموعة.
    ༄
                """)
        else:
            return message.reply("⇜ الأمر هذا يخص ( الأدمنية وفوق بس )")
