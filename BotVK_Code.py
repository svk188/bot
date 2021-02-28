import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
from Raspisanie import groups_list,week_days,groups
from datetime import datetime, timedelta
import locale
from Corona import str_res

def gruppa(response):
    for x in groups_list:
        slovo = x.lower()
        if response == slovo:
            return True


def outputPari(Para,NumberCouple):
    proverka1 = Para.get('subject')
    if proverka1 != "":
        para1 = str(NumberCouple) + ") " + Para.get('subject')+ (" ") + \
                Para.get('lesson_type')+ (" ") + \
                Para.get('lecturer')+ (" ") + \
                Para.get('classroom')+ (" ") + \
                Para.get('url') + "\n"
        return para1
    else:
        Non = str(NumberCouple) + ") " + "--" + "\n"
        return Non

def GruppaPoNedeli(response):
    nedeli = ["понедельник","вторник", "среда", "четверг", "пятница","суббота"]
    bot = "бот"
    for ned in nedeli:
        for i in groups_list:
            slovo = i.lower()
            if response == bot + " " + ned + " " + slovo:
                return True
def Nedeli(response):
    nedeli = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    bot = "бот"
    for ned in nedeli:
        if response == bot + " " + ned:
            return True

def Raspisanie(num,ned,nomer,chet):
    lst = []
    for i in range(6):
        para = groups[num][ned][nomer][chet]
        nomer += 1
        one1 = outputPari(para, nomer)
        lst.append(one1)
    string = ' '.join(lst)
    return string


def main():
    nomer = 0
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') # для получения даты на русском
    vk_session = vk_api.VkApi(token='943d976fd89420888a69ccdeba641e48f71dc04095ca8efe0d77dc72f37574298c4e50dbc517bbb63bf8e')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    Week = datetime.today().weekday()
    wek = (week_days[Week]) # название недели
    today = datetime.today()
    numweek = today.strftime("%U")
    numberweek = int(numweek)-5 # номер недели
    tommorow = today + timedelta(days=1) #завтра
    upload = VkUpload(vk_session)
    attachments = []
    photo = upload.photo_messages(photos="Covid.png")[0]
    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            respons = event.text
            response = respons.lower()
            keyboard = VkKeyboard(one_time=False)
            proverka_gruppi = gruppa(response)
            groupWeek = GruppaPoNedeli(response)
            proverkaNedeli = Nedeli(response)
            if proverka_gruppi == True:
                num = response.upper()
                nomer += 1
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Я запомнил вашу группу " + num)
            elif response == "показать расписание":
                if(nomer != 0):
                    keyboard.add_button('на сегодня', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('на завтра', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_line()
                    keyboard.add_button('на прошлую неделю   ', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('на эту неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button('какая неделя?', color=VkKeyboardColor.DEFAULT)
                    keyboard.add_button('какая группа?', color=VkKeyboardColor.DEFAULT)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard = keyboard.get_keyboard(),
                        message = 'Показываю расписание для группы ' + num)
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Укажите вашу группу. Например ИКБО-01-19')
            elif(response == "привет"):
                vk.messages.send(
                user_id = event.user_id,
                random_id = get_random_id(),
                message = 'Привет, ' + \
                vk.users.get(user_id = event.user_id)[0]['first_name'])
            elif(response == "на сегодня"):
                if nomer != 0:
                    if wek != "SUN":
                        if int(numberweek) % 2 == 0:
                            string = Raspisanie(num,wek,0,1)
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="Показываю раписание на " + today.strftime("%x") + ": " "\n" + \
                                        string)
                        else:
                            string = Raspisanie(num,wek,0,0)
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="Показываю раписание на " + today.strftime("%x") + ": " "\n" + \
                                        string)
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Сегодня воскресенье!")
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Укажите вашу группу. Например ИКБО-01-19")
            elif(response == "на завтра"):
                wek2 = (week_days[Week - 6])
                if nomer != 0:
                    if wek2 != "SUN":
                        if int(numberweek) % 2 == 0:
                            k = Raspisanie(num,wek2,0,1)
                            vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Показываю раписание на " + tommorow.strftime("%x") + ": " "\n" + \
                                    k)
                        else:
                            k = Raspisanie(num,wek2,0,0)
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="Показываю раписание на " + tommorow.strftime("%x") + ": " "\n" + \
                                        k)

                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Завтра воскресенье!")
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Укажите вашу группу. Например ИКБО-01-19')
            elif(response == "на прошлую неделю"):
                if nomer != 0:
                    if (numberweek-1) % 2 == 0:
                        stringMon = Raspisanie(num,"MON",0,1)
                        stringTue = Raspisanie(num,"TUE",0,1)
                        stringWed = Raspisanie(num,"WED",0,1)
                        stringThu = Raspisanie(num,"THU",0,1)
                        stringFri = Raspisanie(num,"FRI",0,1)
                        stringSat = Raspisanie(num,"SAT",0,1)

                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Показываю раписание на неделю: " + str(numberweek-1) + "\n" + \
                                    stringMon +
                                    "Вторник:" + "\n" +
                                    stringTue +
                                    "Среда:" + "\n" +
                                    stringWed +
                                    "Четверг:" + "\n" +
                                    stringThu +
                                    "Пятница:" + "\n" +
                                    stringFri +
                                    "Cуббота:" + "\n" +
                                    stringSat)
                    else:
                        stringMon = Raspisanie(num, "MON", 0, 0)
                        stringTue = Raspisanie(num, "TUE", 0, 0)
                        stringWed = Raspisanie(num, "WED", 0, 0)
                        stringThu = Raspisanie(num, "THU", 0, 0)
                        stringFri = Raspisanie(num, "FRI", 0, 0)
                        stringSat = Raspisanie(num, "SAT", 0, 0)

                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Показываю раписание на прошлую неделю: "+ str(numberweek-1) + "\n" + \
                                    stringMon +
                                    "Вторник:" + "\n" +
                                    stringTue +
                                    "Среда:" + "\n" +
                                    stringWed +
                                    "Четверг:" + "\n" +
                                    stringThu +
                                    "Пятница:" + "\n" +
                                    stringFri +
                                    "Cуббота:" + "\n" +
                                    stringSat)
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Укажите вашу группу. Например ИКБО-01-19')
            elif(response == "на эту неделю"):
                if nomer != 0:
                    if numberweek % 2 == 0:
                        stringMon = Raspisanie(num, "MON", 0, 1)
                        stringTue = Raspisanie(num, "TUE", 0, 1)
                        stringWed = Raspisanie(num, "WED", 0, 1)
                        stringThu = Raspisanie(num, "THU", 0, 1)
                        stringFri = Raspisanie(num, "FRI", 0, 1)
                        stringSat = Raspisanie(num, "SAT", 0, 1)

                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Показываю раписание на неделю: " + "\n" + \
                                    stringMon +
                        "Вторник:" + "\n" +
                                    stringTue +
                        "Среда:" + "\n" +
                                    stringWed +
                        "Четверг:" + "\n" +
                                    stringThu +
                        "Пятница:" + "\n" +
                                    stringFri +
                        "Cуббота:" + "\n" +
                                    stringSat)

                    else:
                        stringMon = Raspisanie(num, "MON", 0, 0)
                        stringTue = Raspisanie(num, "TUE", 0, 0)
                        stringWed = Raspisanie(num, "WED", 0, 0)
                        stringThu = Raspisanie(num, "THU", 0, 0)
                        stringFri = Raspisanie(num, "FRI", 0, 0)
                        stringSat = Raspisanie(num, "SAT", 0, 0)

                    vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Показываю раписание на эту неделю: " + "\n" + \
                                    stringMon +
                                    "Вторник:" + "\n" +
                                    stringTue +
                                    "Среда:" + "\n" +
                                    stringWed +
                                    "Четверг:" + "\n" +
                                    stringThu +
                                    "Пятница:" + "\n" +
                                    stringFri +
                                    "Cуббота:" + "\n" +
                                    stringSat)
                else:
                    vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Укажите вашу группу. Например ИКБО-01-19')
            elif(proverkaNedeli == True):
                if nomer != 0:
                    week = re.findall(r'понедельник|вторник|среда|четверг|пятница|суббота', response)
                    for j in week:
                        n = j
                    if n == "понедельник":
                        k = 'MON'
                    if n == "вторник":
                        k = 'TUE'
                    if n == "среда":
                        k = 'WED'
                    if n == "четверг":
                        k = 'THU'
                    if n == "пятница":
                        k = 'FRI'
                    if n == "суббота":
                        k = 'SAT'
                    string1 = Raspisanie(num, k, 0, 1)

                    string2 = Raspisanie(num, k, 0, 0)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Показываю раписание на чет. "+ n + "\n" + \
                                string1
                                 +"\n"
                    "нечет. " + n + "\n"
                                  +"\n" +
                                string2)
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Укажите вашу группу. Например ИКБО-01-19')
            elif(groupWeek == True):
                group = re.findall(r'(?:\w+)(?:\-\d+\-\d+)', response)
                for i in group:
                    Group = i.upper()
                week = re.findall(r'понедельник|вторник|среда|четверг|пятница|суббота', response)
                for j in week:
                    weeek = j
                if weeek == "понедельник":
                    k = 'MON'
                if weeek == "вторник":
                    k = 'TUE'
                if weeek == "среда":
                    k = 'WED'
                if weeek == "четверг":
                    k = 'THU'
                if weeek == "пятница":
                    k = 'FRI'
                if weeek == "суббота":
                    k = 'SAT'
                string1 = Raspisanie(Group, k, 0, 1)
                string2 = Raspisanie(Group, k, 0, 0)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Показываю раписание для группы "+ Group + " на чет. " + weeek + "\n" + \
                            string1
                                             +  "\n"
                "нечет. " +  "\n"
                             + "\n" +
                            string2)
            elif(response == "какая неделя?"):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Cейчас идет " + str(numberweek) + " неделя")
            elif(response == "какая группа?"):
                if nomer != 0:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Показываю расписание для группы: " + num)
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Укажите вашу группу. Например ИКБО-01-19')
            elif(response == "команды"):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Для начала введите свою группу. Например ИКБО-01-19" + "\n" 
                            "\Показать расписание - появится клавиатура" + "\n" 
                             "\ДЕНЬ ДЕНЕЛИ + НОМЕР ГРУППЫ(Бот вторник ИКБО-01-19) - вам покажет расписание на выбранный вами день и группу" + "\n"
                 "\ДЕНЬ НЕДЕЛИ (Бот вторник) - вам покажет расписание на выбранный вами день у сохраненной группы" +"\n"
                "\Ковид - статистика коронавируса")
            elif(response == "ковид"):
                vk.messages.send(
                    user_id = event.user_id,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message = str_res)
            else:
                vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message= "Неизвестная команда")


if __name__ == '__main__':
    main()