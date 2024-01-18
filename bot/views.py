from contextlib import closing

from django.db import connection
from methodism.helper import dictfetchall, dictfetchone

from bot.Global import Text, BTN, ERROR, FormatText
from bot.btns import inline, key_btn
from bot.models import Category, Product, Cart
from core.models import User as TgUser, ClassRooms, Subject, Quiz, Tests, Variant, AllTests
from telegram import Update, Bot

from bot.tg_admin import admin_msg_handler, admin_inline_handler, admin_img_handler


# Create your views here.

def change_lang(update: Update, context: Bot):
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    update.message.reply_text(Text['STEP1'], reply_markup=inline('lang'))
    user.log = {"state": 'lang'}
    user.save()
    return 0

def start(update: Update, context: Bot):
    tg_user = update.message.from_user
    user = TgUser.objects.get_or_create(user_id=tg_user.id)[0]
    # print(">>>>>>>>>.1")
    # print(user.log["state"])
    # print(type(user.log['state']))
    # print(update.message.chat_id)
    # if user.is_admin:
    #     # print(">>>>>>>>>.a")
    #     update.message.reply_text("Admin panelga xush kelibsz", reply_markup=key_btn('admin', lang=user.lang))
    #     user.log = {"state": 100}
    #     user.save()
    #     return 0

    # print(type(user.log['state']) is int and user.log['state'] < 10)
    # print(">>>>>>>>>>>>.", user.log['state'] is int)
    # print(">>>>>>>>>>>>.", user.log['state'] < 10)
    if type(user.log['state']) is int and user.log['state'] < 10:
        # print(">>>>>>>>>.2")
        update.message.reply_text(Text['START'], reply_markup=inline('lang'))
        user.log = {"state": 1}
        user.username = tg_user.username
        user.save()
        return 0

    else:
        # print(">>>>>>>>>.3")
        update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
        user.log = {"state": 10}
        user.save()
        return 0


def msg_handler(update: Update, context):
    msg = update.message.text
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    # if user.is_admin:
    #     admin_msg_handler(update, context, user, msg, log)
    #     return 0
    #
    # elif msg == 'admin':
    #     update.message.reply_text("Parolni kiriting👇👇👇")
    #     user.log = {"state": 'password'}
    #     user.save()
    #     return 0
    #
    # elif log['state'] == 'password':
    #     if msg == "123":
    #         user.is_admin = True
    #         user.log = {"state": 100}
    #         user.save()
    #         update.message.reply_text("Admin panelga xush kelibsz", reply_markup=key_btn('admin', lang=user.lang))
    #         context.bot.send_message(
    #             text=f"{user.username} | {user.ism} | {tg_user.id}\nUshbu user hozirgina Admin Panelga kirdi",
    #             chat_id=1475094695)
    #         return 0
    #     else:
    #         update.message.reply_text("Parol xato")
    #         return 0

    if msg in BTN["Back"].values():
        if log['state'] == 13:
            sub = Subject.objects.filter(id=log["sub"]).first()
            if not sub:
                update.message.reply_text(Text['CTGError'][user.lang])
                return 0

            markup = key_btn('tests', ctg=sub, lang=user.lang)
            if not markup.keyboard:
                update.message.reply_text(ERROR["TestNotFount"][user.lang])
                return 0

            update.message.reply_text(Text["ChooseQuiz"][user.lang], reply_markup=markup)
            # img = sub.img.path
            # update.message.reply_photo(open(img, 'rb'), caption=ctg.name, reply_markup=markup)
            log['state'] = 12
            log['sub'] = sub.id
            user.log = log
            user.save()
            return 0

            # update.message.reply_text(Text['Prods'][user.lang])
        elif log['state'] == 12:
            update.message.reply_text(Text['CTG'][user.lang], reply_markup=key_btn('ctg'))
            user.log = {"state": 11}
            user.save()
            return 0
        elif log['state'] == 11:
            update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            user.log = {"state": 10}
            user.save()
            return 0.
        elif log["state"] == 2:
            update.message.reply_text(Text['START'], reply_markup=inline('lang'))
            user.log = {"state": 1}
            user.username = tg_user.username
            user.save()
            return 0
        elif log['state'] == 3:
            update.message.reply_text(Text['STEP2'][user.lang])
            user.log = {"state": 2}
            user.save()
            return 0
        elif log["state"] == 20:
            update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            user.log = {"state": 10}
            user.save()
            return 0
        elif log["state"] == 21:
            update.message.reply_text(Text["ClassRoom"][user.lang], reply_markup=key_btn("class", lang=user.lang))
            log["state"] = 20
            user.log = log
            user.save()
            return 0

    elif msg in BTN['bosh-menu'].values():
        update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
        user.log = {"state": 10}
        user.save()
        return 0

    elif msg in BTN['MENU']['menu'].values():
        update.message.reply_text(Text['CTG'][user.lang], reply_markup=key_btn('ctg', lang=user.lang))
        user.log = {"state": 11}
        user.save()

    elif msg in BTN["MENU"]["comp-tests"].values():
        if user.is_admin or user.ut != 3:
            update.message.reply_text(Text["ClassRoom"][user.lang], reply_markup=key_btn("class", lang=user.lang))
            log["state"] = 20
            user.log = log
            user.save()
            return 0

        else:
            update.message.reply_text(Text['Completed-Tests'][user.lang])
            tests = AllTests.objects.filter(user=user).order_by("id")
            for i in tests:
                # update.message.reply_text(f"Bajarilgan Vaqt: {i.created} \nFan: {i.Subject}\nUser: {i.user.full_name()}\nBall: {i.all_balls}\nTest: {i.test.name}")
                update.message.reply_text(FormatText["Comp-Tests"][user.lang].format(i.created, i.Subject, i.user.full_name(), i.all_balls, i.test.name))
            return 0

    elif msg in BTN["MENU"]["set"].values():
        change_lang(update, context)
        return 0

    elif log['state'] == 1:
        update.message.reply_text(Text['STEP1'], reply_markup=inline('lang'))
        return 0

    elif log['state'] == 2:
        if msg.isalpha():
            user.first_name = msg
            user.log = {"state": 3}
            user.save()
            update.message.reply_text(Text['STEP3'][user.lang])
        else:
            update.message.reply_text(Text['STEP2Error'][user.lang])
        return 0

    elif log['state'] == 3:
        if msg.isalpha():
            user.last_name = msg
            user.log = {"state": 4}
            user.save()
            update.message.reply_text(Text['STEP4'][user.lang], reply_markup=key_btn('contact', lang=user.lang))
        else:
            update.message.reply_text(Text['STEP3Error'][user.lang])
        return 0

    elif log['state'] == 4:
        update.message.reply_text(Text['STEP4Error'][user.lang])
        return 0

    elif log['state'] == 5:
        clas = ClassRooms.objects.filter(name=msg).first()
        if clas:
            update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            user.classroom = clas
            user.log = {"state": 10}
            user.save()
            return 0

        else:
            update.message.reply_text(ERROR["ClassRoomNotFount"][user.lang],
                                      reply_markup=key_btn("class", lang=user.lang))
            return 0

    elif log['state'] == 11:
        sub = Subject.objects.filter(name=msg).first()
        if not sub:
            update.message.reply_text(Text['CTGError'][user.lang])
            return 0

        markup = key_btn('tests', ctg=sub, lang=user.lang)
        if not markup.keyboard:
            update.message.reply_text(ERROR["TestNotFount"][user.lang])
            return 0

        update.message.reply_text(Text["ChooseQuiz"][user.lang], reply_markup=markup)
        # img = sub.img.path
        # update.message.reply_photo(open(img, 'rb'), caption=ctg.name, reply_markup=markup)
        log['state'] = 12
        log['sub'] = sub.id
        user.log = log
        user.save()
        return 0

        # update.message.reply_text(Text['Prods'][user.lang])

    elif log['state'] == 12:
        prod = Tests.objects.filter(name=msg).first()
        if not prod:
            update.message.reply_text(ERROR["TestNotFount"][user.lang])
            return 0
        quizs = Quiz.objects.filter(test=prod)
        b = 0
        for i in quizs:
            b += i.ball

        s = f"""
        Nomi: {prod.name}\n
        Ishlash vaqti: {prod.timeout}\n
        Test soni: {len(quizs)}\n
        Obshiy ball: {b}
        """
        update.message.reply_text(s, reply_markup=key_btn('test-conf', lang=user.lang))
        # update.message.reply_text("fdhj")
        # update.message.reply_text("Quyidagilardan birini tanlang👇👇", reply_markup=key_btn('prod', lang=user.lang))
        log['state'] = 13
        log['tests'] = prod.id
        user.log = log
        user.save()
        return 0

    elif log["state"] == 13:
        if msg == "GO":
            quiz = Quiz.objects.filter(test_id=log["tests"])
            s = F"№1\nSavol: {quiz[0].name}\n{quiz[0].desc}\nBall: {quiz[0].ball}"
            s = FormatText["Quiz"][user.lang].format(1, quiz[0].name, quiz[0].desc, quiz[0].ball)
            # print(">>>>>>>>>>>>", quiz.img)
            if quiz[0].img:
                # pass  # to be continued
                update.message.reply_photo(open(quiz[0].img.path, 'rb'), caption=s,
                                           reply_markup=key_btn('variant', quiz=quiz[0], lang=user.lang))
                log["state"] = 14
                log["quiz"] = 1
                log["ball"] = 0
                log["trueAnswers"] = 0
                log["lastQuiz"] = len(quiz)
                user.log = log
                user.save()
                return 0
            else:
                update.message.reply_text(s, reply_markup=key_btn('variant', quiz=quiz[0], lang=user.lang))
                # print(">>>>>>>", len(quiz))
                log["state"] = 14
                log["quiz"] = 1
                log["trueAnswers"] = 0
                log["ball"] = 0

                log["lastQuiz"] = len(quiz)
                # print(">>>>>", log)
                user.log = log
                user.save()
                # print(">>>>>", user.log)
                return 0
        else:
            update.message.reply_text(Text["MENU"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            user.log = {"state": 10}
            user.save()
            return 0

    elif log["state"] == 14:
        if msg in BTN["StopTest"].values():
            update.message.reply_text(Text["TestEnd"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            tests = Quiz.objects.filter(test_id=log["tests"])
            # s = f"Ball: {log['ball']} \nTogri javoblar: {log['trueAnswers']}\nObshiy savolar: {len(tests)}\nNotori javoblar: {len(tests)-log['trueAnswers']}"
            # s = f"Ball: {log['ball']} \nTogri javoblar: {log['trueAnswers']}"
            # print(Text['STEP2Error'][user.lang], type(Text['STEP2Error'][user.lang]))
            # print(ERROR["TestEnd"][user.lang], type(ERROR["TestEnd"][user.lang]))
            # print(FormatText["TestEnd"][user.lang], type(FormatText["TestEnd"][user.lang]))
            # print(str(FormatText["TestEnd"][user.lang], type(FormatText["TestEnd"][user.lang])))
            update.message.reply_text(str(FormatText["TestEnd"][user.lang]).format(log['ball'], log['trueAnswers'], len(tests), len(tests)-log['trueAnswers']))
            AllTests.objects.create(Subject_id=log['sub'], test_id=log['tests'], user=user, all_balls=log["ball"])
            user.log = {"state": 10}
            user.save()
            return 0

        quiz = Quiz.objects.filter(test=log["tests"])
        variant = Variant.objects.filter(test=quiz[log["quiz"] - 1], answer=msg).first()
        if variant is None:
            update.message.reply_text("Xato variant!")
            # s = F"№{log['quiz']}\nSavol: {quiz[log['quiz'] - 1].name}\n{quiz[log['quiz'] - 1].desc}\nBall: {quiz[log['quiz'] - 1].ball}"
            s = FormatText["Quiz"][user.lang].format(log['quiz'], quiz[log['quiz'] - 1].name, quiz[log['quiz'] - 1].desc, quiz[log['quiz'] - 1].ball)
            if quiz[log['quiz'] - 1].img:
                update.message.reply_photo(open(quiz[log['quiz'] - 1].img.path, 'rb'), caption=s,
                                           reply_markup=key_btn('variant', quiz=quiz[log['quiz'] - 1], lang=user.lang))
                return 0

            elif not quiz[log['quiz'] - 1].img:
                update.message.reply_text(s,
                                          reply_markup=key_btn('variant', quiz=quiz[log['quiz'] - 1], lang=user.lang))
                return 0

        # print("here")
        # print(variant)
        # print("????", variant.is_true)
        # print(">>>>>>>>>>", log["quiz"] <= log["lastQuiz"])
        if variant.is_true:
            # print(">>>", 1)
            # print("--------------------------------", quiz[log["quiz"]-1].ball)
            log["ball"] += quiz[log["quiz"] - 1].ball
            log["trueAnswers"] += 1
            user.log = log
            user.save()
        # print(">>>", 2)
        if log["quiz"] >= log["lastQuiz"]:
            # print(">>>", 2.1)
            update.message.reply_text(Text["TestEnd"][user.lang], reply_markup=key_btn("menu", lang=user.lang))
            tests = Quiz.objects.filter(test_id=log["tests"])
            update.message.reply_text(
                str(FormatText["TestEnd"][user.lang]).format(log['ball'], log['trueAnswers'], len(tests),
                                                             len(tests) - log['trueAnswers']))

            AllTests.objects.create(Subject_id=log['sub'], test_id=log['tests'], user=user, all_balls=log["ball"])
            user.log = {"state": 10}
            user.save()
        else:
            # print(">>>", 3)
            s = FormatText["Quiz"][user.lang].format(log['quiz'], quiz[log['quiz'] - 1].name,
                                                     quiz[log['quiz'] - 1].desc, quiz[log['quiz'] - 1].ball)
            if quiz[log['quiz']].img:
                update.message.reply_photo(open(quiz[log['quiz']].img.path, 'rb'), caption=s,
                                           reply_markup=key_btn('variant', quiz=quiz[log['quiz']], lang=user.lang))
            elif not quiz[log['quiz']].img:
                update.message.reply_text(s, reply_markup=key_btn('variant', quiz=quiz[log['quiz']], lang=user.lang))

        log["quiz"] += 1
        # print(log)
        user.log = log
        user.save()
        return 0

    elif log["state"] == 20:
        update.message.reply_text(Text["ChoosePupil"][user.lang], reply_markup=key_btn("pupil", lang=user.lang, ctg=msg))
        log["state"] = 21
        user.log = log
        user.save()
        return 0

    elif log["state"] == 21:
        user = TgUser.objects.filter(first_name=msg).first()
        update.message.reply_text(Text['Completed-Tests'][user.lang])
        tests = AllTests.objects.filter(user=user).order_by("id")
        for i in tests:
            # update.message.reply_text(f"Bajarilgan Vaqt: {i.created} \nFan: {i.Subject}\nUser: {i.user.full_name()}\nBall: {i.all_balls}\nTest: {i.test.name}")
            update.message.reply_text(
                FormatText["Comp-Tests"][user.lang].format(i.created, i.Subject, i.user.full_name(), i.all_balls,
                                                           i.test.name))
        log["state"] = 10
        user.log = log
        user.save()
        return 0


def photo_handler(update: Update, context):
    photo = update.message.photo
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    if user.is_admin:
        admin_img_handler(update, context, user, photo, log)
        return 0
    update.message.reply_text("Hozircha Bu ishlamayabdi")
    return 0


def contact_hand(update: Update, context: Bot):
    contact = update.message.contact
    tg_user = update.message.from_user
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log
    if log['state'] == 4:
        update.message.reply_text("Class: ", reply_markup=key_btn("class", lang=user.lang))
        user.phone = contact.phone_number
        user.log = {"state": 5}
        user.save()
        return 0


def inline_handler(update: Update, context):
    query = update.callback_query
    data = query.data
    tg_user = query.message.chat
    user = TgUser.objects.get(user_id=tg_user.id)
    log = user.log

    data_sp = data.split('_')
    if user.is_admin:
        admin_inline_handler(query, context, user, data, log, data_sp)
        return 0

    if data_sp[0] == 'plus':
        son = int(data_sp[2]) + 1
        prod = Product.objects.filter(id=int(data_sp[1])).first()
        s = f"""Nomi: {prod.name}\nTarkibi: {prod.tarkibi}\nNarxi: {prod.price * son} so'm"""
        query.message.edit_caption(caption=s, reply_markup=inline("prod", product_id=prod.id, count=son))
        return 0
    elif data_sp[0] == 'minus':
        if int(data_sp[2]) == 1:
            query.answer("Yetib kelding boshqa bosib bo'maydi")
            return 0
        son = int(data_sp[2]) - 1
        prod = Product.objects.filter(id=int(data_sp[1])).first()
        s = f"""Nomi: {prod.name}\nTarkibi: {prod.tarkibi}\nNarxi: {prod.price * son} so'm"""
        query.message.edit_caption(caption=s, reply_markup=inline("prod", product_id=prod.id, count=son))
        return 0
    elif data_sp[0] == "nothing":
        query.answer("Bu yerni bosish befoyda")
        return 0

    elif data_sp[0] == "cart":
        cart = Cart.objects.get_or_create(user_id=tg_user.id, product_id=int(data_sp[1]))[0]
        cart.quent = int(data_sp[2]) + cart.quent
        cart.save()
        query.message.delete()
        query.message.reply_text("Savatga qo'shildi", reply_markup=key_btn('menu', lang=user.lang))
        user.log = {"state": 10}
        user.save()
        return 0

    elif log['state'] == 1:
        query.message.delete()
        user.lang = data
        query.message.reply_text(Text['STEP2'][data])
        user.log = {"state": 2}
        user.save()
        return 0
    elif log['state'] == 'lang':
        query.message.delete()
        query.message.reply_text(Text['SUCCESS_LANG'][data], reply_markup=key_btn('menu', lang=data))
        user.lang = data
        user.log = {"state": 10}
        user.save()
        return 0
