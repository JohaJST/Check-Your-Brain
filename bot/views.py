from contextlib import closing

from django.db import connection
from methodism.helper import dictfetchall, dictfetchone

from core.models import User, TG_User, ClassRooms
from telegram import Update, Bot
from bot.btn import key_btn


def start(update: Update, context: Bot):
    tg_user = update.message.from_user
    user = TG_User.objects.get_or_create(user_id=tg_user.id)[0]
    if user.log["state"] >= 2:
        update.message.reply_text("Menu", reply_markup=key_btn("menu"))
        user.log["state"] = 3
        user.save()
        return 0

    update.message.reply_text("Отправьте номер", reply_markup=key_btn("contact"))
    user.first_name = tg_user.first_name
    user.last_name = tg_user.last_name
    user.username = tg_user.username
    user.log["state"] = 2
    user.save()
    return 0


def msg_handler(update: Update, context):
    msg = update.message.text
    tg_user = update.message.from_user
    user = TG_User.objects.get(user_id=tg_user.id)
    log = user.log
    # print(1)
    if log["state"] == 3:
        update.message.reply_text("Выберите класс", reply_markup=key_btn("classrooms"))
        log["state"] = 4
        user.save()
        return 0
    elif log["state"] == 4:
        update.message.reply_text("Выберите ученика(цы)", reply_markup=key_btn("user", ctg=msg))
        log["state"] = 5
        user.save()
    # print(3)
    return 0


def contact_hand(update: Update, context: Bot):
    contact = update.message.contact
    tg_user = update.message.from_user
    user = TG_User.objects.get(user_id=tg_user.id)
    if user.log["state"] == 2 and contact.user_id == user.user_id:
        update.message.reply_text("Menu", reply_markup=key_btn("menu"))
        user.phone = contact.phone_number
        user.log["state"] = 3
        user.save()
        return 0
    update.message.reply_text("Отправьте номер", reply_markup=key_btn("contact"))
    return 0
