# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs

from cokkies import get_cokie_and_user_agent
from sheet import worksheet
cookie_m = None
user_agent_m = None
minus_word = 'Центр дистанционных торгов;Аукционный тендерный центр;Аукционы Сибири;Межрегиональная Электронная Торговая Система;Фабрикант;Альфалот;Уральская;электронная торговая площадка;Tender Technologies;Электронная площадка ЭСП;Профит;Вердиктъ;Сбербанк-АСТ;Центра реализации;Новые информационные сервисы;Российский аукционный дом;Электронная торговая площадка "Регион";Всероссийская Электронная;Торговая Площадка;Аукцион-центр;Региональная Торговая площадка;ELECTRO-TORGI.RU;ТП "Фабрикант";АО «Сбербанк-АСТ»;uTender;"Новые информационные сервисы";Вердиктъ;Всероссийская Электронная Торговая Площадка;RUSSIA OnLine;Электронная площадка Центра реализации;Систематорг;Сибирская торговая площадка;Уральская электронная торговая площадка;ПТП-Центр;ТендерСтандарт;Электронная торговая площадка "Профит";«Региональная Торговая площадка»;ПТП-Центр;АКОСТА info;Балтийская электронная площадка;ЭТП "ЮГРА";Электронная торговая площадка ELECTRO-TORGI.RU;Мета-инвест;Объединенная Торговая Площадка;"Арбитат";«RUSSIA OnLine»;"ПТП-Центр";Электронная площадка "Аукционный тендерный центр";«Электронная торговая площадка ELECTRO-TORGI.RU»;"Всероссийская Электронная Торговая Площадка";«Новые информационные сервисы»;«Электронная площадка «Вердиктъ»;ООО «Центр реализации»;"Ru-Trade24";ЭТП "Пром-Консалтинг";Электронная торговая площадка УТП Сбербанк-АСТ;Электронная торговая площадка "Евразийская торговая площадка";"Аукционы Сибири";"Сибирская торговая площадка";«Системы ЭЛектронных Торгов»;ЭТП "Пром-Консалтинг";МЕТА-ИНВЕСТ;ООО «Специализированная организация по проведению торгов – Южная Электронная Торговая Площадка»;«ТЕНДЕР ГАРАНТ»;"Сибирская торговая площадка";B2B-Center;"Открытая торговая площадка";«Property Trade»;ЭТП "МЕЖРЕГИОНАЛЬНАЯ ЭЛЕКТРОННАЯ ТОРГОВАЯ СИСТЕМА";Электронная площадка "Система Электронных Торгов Имуществом" (СЭЛТИМ);ТП "Фабрикант" (www.fabrikant.ru);"Открытая торговая площадка";B2B-Center'

minus_word = minus_word.strip().split(";")


def pdf_pars(cookie=None,user_agent=None,id=None):
    global cookie_m,user_agent_m
    try:
        if not cookie or not user_agent :
            cookie,user_agent,_ = get_cokie_and_user_agent(None)
            cookie_m = cookie
            user_agent_m = user_agent
            return pdf_pars(cookie=cookie,user_agent=user_agent,id=id)
        cookies = {
            'bankrotcookie': cookie,
            'ASP.NET_SessionId': 'z0e1txqjs5n4culpwn54udpz',
        }
        headers = {
            'User-Agent': user_agent,
        }

        params = {
            'ID': id}
        start_date = ""
        lot_id= ""
        start_place= ""
        while True:
            try:
                response = requests.get('https://old.bankrot.fedresurs.ru/MessageWindow.aspx', params=params, cookies=cookies, headers=headers,timeout=5)
                break
            except:
                print("PASS PDF")
                pass
        if len(response.text) < 2000:   
            cookie,user_agent,id = get_cokie_and_user_agent(id)
            cookie_m = cookie
            user_agent_m = user_agent
            return pdf_pars(cookie=cookie,user_agent=user_agent,id=id)
        soup = bs(response.text,"lxml")
        name = soup.find("table").find("h1",class_="red_small").text.strip()
        span = soup.find("span",id="ctl00_BodyPlaceHolder_lblBody")
        inf = span.find_all("table",class_="headInfo")[1].find_all("tr")

        message_number = span.find("table").find("tr").find_all("td")[-1].text.strip()
        start_date = span.find("table",class_="headInfo").find_all("tr")[1].find_all("td")[1].text.strip()

        full_name = inf[0].find_all("td")[1].text.strip()
        born_place = inf[3].find_all("td")[0].text.strip()
        if "Место" in  born_place:
            born_place = inf[3].find_all("td")[1].text.strip()
        else:
            born_place = ""
        made_by = " ".join(span.find_all("table",class_="headInfo")[2].find("tr").find_all("td")[1].text.strip().split())
        if name == "Иное сообщение":
            lot = "Лот"+span.find("div",class_="msg").text.split("Лот"or "ЛОТ" or "лот",1)[1][:30] if len(span.find("div",class_="msg").text.split("Лот"or "ЛОТ",1)) > 1 else ""
        else:
            lot_id,lot = [x.text.strip() for x in span.find("table",class_="lotInfo").find_all("tr")[1].find_all("td")[:2]]
            start_place = span.find_all("table",class_="headInfo")[3].find_all("tr")[-1].find_all("td")[1].text.strip()
        
        data = {
            "message_number":message_number,
            "full_name":full_name,
            "born_place":born_place,
            "made_by":made_by,
            "lot":lot,
            "lot_id":"No "+lot_id+ " " if lot_id != "" else "",
            "start_date":start_date,
            "start_place":start_place
        }
        made_by = made_by.split("(")[0] if len(made_by) > 10 else ""
        print("CHECK",start_place)
        if start_place != "":
            for elem in minus_word:
                if elem in start_place:
                    print(elem," -IN- ",start_place)
                    return
        my_sh = ["https://old.bankrot.fedresurs.ru/MessageWindow.aspx?ID="+id,message_number,start_date,full_name,made_by,born_place,start_place,lot_id+lot]
        # worksheet.insert_row(my_sh,2)
        print("GOOD")
        worksheet.append_row(my_sh)
    except:
        print("Some error")


def main(page=1,last_page=0):
    global cookie_m,user_agent_m
    print(page,last_page)
    links_in_sheet = worksheet.col_values(1)

    if int(page) > int(last_page) and int(last_page) != 0: return
    while True:
        try:
            # r = requests.get(f"https://tbankrot.ru/reestr?page={page}&type=mess&text=%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6+&debtor=&dt_1=20.08.2022&dt_2=20.08.2022&t%5B%5D=2&t%5B%5D=7",timeout=5)
            r = requests.get(f"https://tbankrot.ru/reestr?page={page}&type=mess&text=%D0%BF%D1%80%D1%8F%D0%BC&debtor=&dt_1=20.08.2022&dt_2=20.08.2022&t%5B%5D=2&t%5B%5D=7",timeout=5)
            break
        except:
            print("PASS REQUEST")
            pass
    soup = bs(r.content,"lxml")
    table = soup.find("table",class_="base").find_all("td",class_="show_message_window")
    if  last_page == 0:
        last_page = int(soup.find("ul",class_="pagination").find_all("li")[-1].text)
    for elem in table:
        link = elem["data-rel"].split("=")[1]
        full_link = "https://old.bankrot.fedresurs.ru/MessageWindow.aspx?ID=" + link
        if full_link not in links_in_sheet:
            # print("GO",link)
            pdf_pars(id=link,cookie=cookie_m,user_agent=user_agent_m)
    return main(page =page+1,last_page=last_page)


if __name__ == "__main__":
    main()




