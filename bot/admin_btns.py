from contextlib import closing

from django.db import connection
from methodism import dictfetchone
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def admin_btns(type):
    btn = []
    if type == 'conf':
        btn = [
            [KeyboardButton("❤️‍🩹Ha"), KeyboardButton("🙅‍♂Hazillashdim")]
        ]
    elif type == 'menu':
        btn = [
            [KeyboardButton("🍱Categoriyalar"), KeyboardButton("🍱Maxsulotlar")]
        ]
    elif type == 'create_ctg':
        btn = [
            [KeyboardButton("🆕Yangi Categoriya qo'shish")]
        ]
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def adbtn_inline(type=None, page=1, count=0, ctg=None):
    btn = []
    if type == "ctgs":
        btn = [
            [InlineKeyboardButton("⏮", callback_data=f"ctg_prev_{ctg.id}_{page}"),
             InlineKeyboardButton(f"{page}/{count}", callback_data=f"ctg_none"),
             InlineKeyboardButton("⏭", callback_data=f"ctg_next_{ctg.id}_{page}")],
            [InlineKeyboardButton("✏️Tahrirlash", callback_data=f"ctg_edit_{ctg.id}_{page}")],
            [InlineKeyboardButton("🗑O'chirib tashlash", callback_data=f"ctg_delete_{ctg.id}_{page}")],
        ]
        # offset = (page - 1) * 1
        # sql = f"select * from bot_category limit 1 offset {offset}"
        # cnt = "select count(*) as cnt from bot_category"
        # with closing(connection.cursor()) as cursor:
        #     cursor.execute(sql)
        #     one = dictfetchone(cursor)
        #     cursor.execute(cnt)
        #     cnt = dictfetchone(cursor)
        # btn = [
        #     [InlineKeyboardButton("<", callback_data=f"ctg_{one['id']}_{page}")],
        #     [InlineKeyboardButton(f"{page}/{cnt['cnt']}", callback_data=f"ctg_none")],
        #     [InlineKeyboardButton(">", callback_data=f"ctg_{one['id']}_{page}")],
        # ]
    elif type == "ctg_delete_conf":
        btn = [
            [InlineKeyboardButton("🗑 O'chirish", callback_data=f'ctg_delete_conf_yes_{page}_{ctg.id}'),
             InlineKeyboardButton("🔙Ortga", callback_data=f'ctg_delete_conf_no_{page}_{ctg.id}')]
        ]
    return InlineKeyboardMarkup(btn)
