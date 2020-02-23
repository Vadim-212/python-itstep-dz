currency_pairs = {
    'USD-KZT': 377,
    'EUR-KZT': 410
}


def is_number(num):
    try:
        float(num)
        return True
    except ValueError: return False


def is_currency(curr):
    if len(curr) == 3: return True
    else: return False


def is_currency_pair_exists(curr1,curr2):
    pair = f'{curr1}-{curr2}'
    curr = currency_pairs.get(pair)
    if curr is None: 
        pair = f'{curr2}-{curr1}'
        curr = currency_pairs.get(pair)
        if curr is None: return False
        else: return True
    else: return True


def add_update_currency_pair(curr1,curr2,num1,num2):
    currency_pairs[f'{curr1}-{curr2}'] = round(float(num2) / float(num1), 3)


def get_rate(num,currFrom,currTo):
    result = 0
    curr = currency_pairs.get(f'{currFrom}-{currTo}')
    if curr is None:
        curr = currency_pairs.get(f'{currTo}-{currFrom}')
        result = float(num) / curr
    else: result = float(num) * curr
    return round(result,3)


while True:
    string = input('>>> ')
    strs = string.split(' ')
    if is_currency(strs[1]) and is_currency(strs[2]) or is_currency(strs[1]) and is_currency(strs[3]):
        if is_number(strs[0]) is False:
            print('Неверное число')
            continue
        if is_currency(strs[1]) and is_currency(strs[2]):
            if is_currency_pair_exists(strs[1],strs[2]):
                result = get_rate(strs[0],strs[1],strs[2])
                print(result)
            else: print('Нет такой валютной пары')
        elif is_currency(strs[1]) and is_currency(strs[3]):
            if is_number(strs[2]) is False:
                print('Неверное число')
                continue
            if is_currency_pair_exists(strs[1],strs[3]):
                add_update_currency_pair(strs[1],strs[3],strs[0],strs[2])
                print('Такая валютная пара уже существует\nКурс обновлен')
            else:
                add_update_currency_pair(strs[1],strs[3],strs[0],strs[2])
                print('Валютная пара добавлена')
    else:
        print('Неверный формат')
