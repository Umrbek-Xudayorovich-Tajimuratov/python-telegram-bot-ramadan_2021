from datetime import datetime, timedelta
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from conf import TOKEN, DB_NAME
from db_create import DBHelper

STATE_CALENDAR = 2
STATE_REGION = 1
opted_region = dict()
db = DBHelper(DB_NAME)

BTN_TODAY, BTN_TOMORROW, BTN_MONTH, BTN_REGION, BTN_DUA = '⏳ Bugun', '⏳ Ertaga', "🗓 To'liq taqvim", "🇺🇿 Mintaqa", "🤲 Duolar"
main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW, BTN_MONTH], [BTN_REGION], [BTN_DUA]
], resize_keyboard=True)


def regions_buttons():
    regions = db.get_regions()
    buttons = []
    tmp_b = []
    for region in regions:
        tmp_b.append(InlineKeyboardButton(region["regions"], callback_data=region["region_id"]))
        if len(tmp_b) == 2:
            buttons.append(tmp_b)
            tmp_b = []
    return buttons


def start(update, context):
    user = update.message.from_user
    opted_region[user.id] = None
    buttons = regions_buttons()
    update.message.reply_html(f"Assalomu Aleykum<b> {user.first_name}</b>!\n"
                              f"<i>Ramazon oyi muborak bo'lsin!</i>",
                              reply_markup=InlineKeyboardMarkup(buttons))

    return STATE_REGION


def inline_buttons_query(update, context):
    query = update.callback_query  # callback_data qaytargan ma'lumot: region_1/region_2 ni oladi
    user_id = query.from_user.id
    opted_region[user_id] = int(query.data)
    query.message.delete()
    query.message.reply_html(f'<b>Ramazon taqvimi!</b> 2️⃣0️⃣2️⃣1️⃣\n'
                             f'Quyidagilardan birini tanlang 👇',
                             reply_markup=main_buttons)
    # query.edit_message_text(text='<b>Ramazon taqvimi!</b> 2️⃣0️⃣2️⃣1️⃣\nQuyidagilardan birini tanlang 👇',
    #                         parse_mode="HTML")
    return STATE_CALENDAR


def calendar_today(update, context):
    user_id = update.message.from_user.id
    if not opted_region[user_id]:
        return STATE_REGION
    opted_region_id = opted_region[user_id]
    region = db.get_region(opted_region_id)
    today = str(datetime.now().date())
    calendar = db.get_calendar_by_region(opted_region_id, today)
    photo_path = f"images/{calendar['id']}.jpg"
    message = f"⛳  <b>{region['regions']}</b>\n<pre>"\
              f"Bugungi Ramazon taqvimi\n-------------------------</pre>\n"\
              f"🔻 <b><i>Saxarlik:</i> |  {calendar['fajr'][:4]}</b>\n"\
              f"🔺 <b><i>Iftorlik:</i>    |  {calendar['maghrib'][:5]}</b>"
    update.message.reply_photo(photo=open(photo_path, "rb"), caption=message,
                               parse_mode="HTML", reply_markup=main_buttons)


def calendar_tomorrow(update, context):
    user_id = update.message.from_user.id
    if not opted_region[user_id]:
        return STATE_REGION
    opted_region_id = opted_region[user_id]
    region = db.get_region(opted_region_id)
    today = str(datetime.now().date() + timedelta(days=1))
    calendar = db.get_calendar_by_region(opted_region_id, today)
    photo_path = f"images/{calendar['id']}.jpg"
    message = f"⛳  <b>{region['regions']}</b>\n<pre>" \
              f"Ertangi Ramazon taqvimi\n-------------------------</pre>\n" \
              f"🔻 <b><i>Saxarlik:</i> |  {calendar['fajr'][:4]}</b>\n" \
              f"🔺 <b><i>Iftorlik:</i>    |  {calendar['maghrib'][:5]}</b>"
    update.message.reply_photo(photo=open(photo_path, "rb"), caption=message,
                               parse_mode="HTML", reply_markup=main_buttons)


def calendar_month(update, context):
    user_id = update.message.from_user.id
    if not opted_region[user_id]:
        return STATE_REGION
    opted_region_id = opted_region[user_id]
    region = db.get_region(opted_region_id)
    photo_path = f"images/table/region_{opted_region_id}.png"
    message = f"⛳  <b>{region['regions']}</b>\n<pre>Oylik Ramazon taqvimi</pre>"
    update.message.reply_photo(photo=open(photo_path, "rb"), caption=message,
                               parse_mode="HTML", reply_markup=main_buttons)


def select_region(update, context):
    buttons = regions_buttons()
    update.message.reply_html(f"<pre>⛳  SIZGA QAYSI MINTAQA HAQIDA MA'LUMOT BERAY?</pre>",
                              reply_markup=InlineKeyboardMarkup(buttons))

    return STATE_REGION


def select_dua(update, context):
    saxarlik = "\nنَوَيْتُ أَنْ أَصُومَ صَوْمَ شَهْرَ رَمَضَانَ مِنَ الْفَجْرِ إِلَى الْمَغْرِبِ، خَالِصًا لِلهِ تَعَالَى أَللهُ أَكْبَرُ" \
        "\n Navaytu an asuma sovma shahri ramazona minal fajri ilal mag‘ribi," \
        "xolisan lillahi ta’ala. Allohu akbar"
    iftorlik = "اَللَّهُمَّ لَكَ صُمْتُ وَ بِكَ آمَنْتُ وَ عَلَيْكَ تَوَكَّلْتُ" \
        "وَ عَلَى رِزْقِكَ أَفْتَرْتُ، فَغْفِرْلِى مَا قَدَّمْتُ وَ مَا أَخَّرْتُ بِرَحْمَتِكَ يَا أَرْحَمَ الرَّاحِمِين " \
       "\n Allohumma laka sumtu va bika amantu va a’layka tavakkaltu va"  \
       "a’laa rizqika aftortu, fag‘firliy ma qoddamtu va maa axxortu"

    update.message.reply_photo(photo=open("images/ramadan_dua.png", "rb"),
                               caption=f"<b>Saxarlik(og'iz yopish): </b>\n{saxarlik}\n\n<b>"
                                       f"Iftorlik(og'iz ochish): \n</b>\n{iftorlik}",
                               parse_mode="HTML", reply_markup=main_buttons)


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # """todo: Start ni ushlab olish uchun ishlatiladi, start bosilganda start func ishlasin"""
    # dispatcher.add_handler(CommandHandler('start', start))
    # """todo: Inlinebuttonlarni ushlab, ular bosilganda nima bo'lishini aytadi. knopka bosilganda inline func iwdi"""
    # dispatcher.add_handler(CallbackQueryHandler(inline_buttons_query))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_REGION: [
                CallbackQueryHandler(inline_buttons_query),
                MessageHandler(Filters.regex('^(' + BTN_TODAY + ')$'), calendar_today),
                MessageHandler(Filters.regex('^(' + BTN_TOMORROW + ')$'), calendar_tomorrow),
                MessageHandler(Filters.regex('^(' + BTN_MONTH + ')$'), calendar_month),
                MessageHandler(Filters.regex('^(' + BTN_REGION + ')$'), select_region),
                MessageHandler(Filters.regex('^(' + BTN_DUA + ')$'), select_dua),
                           ],
            STATE_CALENDAR: [
                MessageHandler(Filters.regex('^('+BTN_TODAY+')$'), calendar_today),
                MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'), calendar_tomorrow),
                MessageHandler(Filters.regex('^('+BTN_MONTH+')$'), calendar_month),
                MessageHandler(Filters.regex('^('+BTN_REGION+')$'), select_region),
                MessageHandler(Filters.regex('^('+BTN_DUA+')$'), select_dua),
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()