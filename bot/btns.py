from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                      ReplyKeyboardMarkup)
from bot.Global import BTN
from bot.models import Category, Product
from core.models import Subject, Quiz, ClassRooms, Tests, Variant, User as TgUser


def key_btn(type, lang='uz', ctg=None, quiz=None):
    btn = []
    if type == 'contact':
        btn = [[KeyboardButton(f"📱{BTN['CONTACT'][lang]}", request_contact=True)]]
    elif type == 'class':
        clas = ClassRooms.objects.all()
        btn = []
        for i in range(1, len(clas), 2):
            btn.append([
                KeyboardButton(clas[i-1].name),
                KeyboardButton(clas[i].name),
            ])

        if len(clas) % 2:
            btn.append(
                [KeyboardButton(clas[len(clas)-1].name)]
            )
        btn.append(
            [
                KeyboardButton(BTN["Back"][lang])
            ],
        )
    elif type == "menu":
        btn = [
            [KeyboardButton(f"{BTN['MENU']['menu'][lang]}")],
            [KeyboardButton(f"{BTN['MENU']['set'][lang]}"), KeyboardButton(f"{BTN['MENU']['comp-tests'][lang]}")],
        ]
    elif type == 'ctg':
        category = Subject.objects.all()
        btn = []
        for i in range(1, len(category), 2):
            btn.append([
                KeyboardButton(category[i-1].name),
                KeyboardButton(category[i].name),
            ])

        if len(category) % 2:
            btn.append(
                [KeyboardButton(category[len(category)-1].name)]
            )
        btn.append(
            [
                KeyboardButton(BTN["Back"][lang]), KeyboardButton(f"{BTN['bosh-menu'][lang]}")
            ],
        )
    elif type == "tests":
        roots = Tests.objects.filter(subject=ctg)
        btn = []
        for i in range(1, len(roots), 2):
            btn.append([
                KeyboardButton(roots[i - 1].name),
                KeyboardButton(roots[i].name),
            ])
        if len(roots) % 2:
            btn.append([KeyboardButton(roots[len(roots) - 1].name)])
        btn.append([KeyboardButton(BTN["Back"][lang]), KeyboardButton(f"{BTN['bosh-menu'][lang]}")],)
    elif type == "test-conf":
        btn = [
            [
                KeyboardButton("GO")
            ],
            [
                KeyboardButton(BTN["Back"][lang]), KeyboardButton(f"{BTN['bosh-menu'][lang]}")
            ]
        ]
    elif type == "admin":
        btn = [
            [KeyboardButton("📝Boshqaruv"), KeyboardButton("📊Foydalanuvchilar ro'yxati")],
            [KeyboardButton("🏘Logout")]
        ]
    elif type == "variant":
        variants = Variant.objects.filter(test=quiz)
        btn = []
        for i in range(1, len(variants), 2):
            btn.append([
                KeyboardButton(variants[i - 1].answer),
                KeyboardButton(variants[i].answer),
            ])

        if len(variants) % 2:
            btn.append(
                [KeyboardButton(variants[len(variants) - 1].answer)]
            )
        btn.append(
            [
                KeyboardButton(BTN["StopTest"][lang]), KeyboardButton(f"{BTN['bosh-menu'][lang]}")
            ],
        )
    elif type == "pupil":
        croom = ClassRooms.objects.filter(name=ctg).first()
        category = TgUser.objects.filter(classroom_id=croom)
        # print(category)
        # print(len(category))
        # print(">>>>>>>", category[0].phone)
        btn = []
        for i in range(1, len(category), 2):
            # print(i)
            btn.append([
                KeyboardButton(category[i-1].first_name),
                KeyboardButton(category[i].first_name),
            ])

        if len(category) % 2:
            btn.append(
                [KeyboardButton(category[len(category)-1].first_name)]
            )
        btn.append(
            [
                KeyboardButton(BTN["Back"][lang]), KeyboardButton(f"{BTN['bosh-menu'][lang]}")
            ],
        )
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def inline(type, product_id=None, count=1):
    btn = []

    if type == "lang":
        btn = [[
            InlineKeyboardButton("🇺🇿Uz", callback_data='uz'),
            InlineKeyboardButton("🇷🇺Ru", callback_data='ru'),
            InlineKeyboardButton("🇺🇸En", callback_data='en'),
        ]]
    elif type == "prod":
        btn = [
            [
                InlineKeyboardButton("-", callback_data=f"minus_{product_id}_{count}"),
                InlineKeyboardButton(f"{count}", callback_data="nothing"),
                InlineKeyboardButton("+", callback_data=f"plus_{product_id}_{count}"),
            ],
            [
                InlineKeyboardButton("🛒Savatga qo'shish", callback_data=f"cart_{product_id}_{count}")
            ]
        ]

    return InlineKeyboardMarkup(btn)
