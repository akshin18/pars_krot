import gspread


gs = gspread.service_account(filename='cr.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('1wV71rqKv9PCjXfFrApMlKTC1fW37KoJjZYksOZ-7RmU')  # подключаем таблицу по ID
worksheet = sh.sheet1  # получаем первый лист





