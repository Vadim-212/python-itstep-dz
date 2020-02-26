currency_pairs = {
    'USD-KZT': 377,
    'EUR-KZT': 410
}


def is_number(num):
    try:
        float(num)
        return True
    except ValueError: 
        return False


def is_currency(curr):
    if len(curr) == 3: 
        return True
    else: 
        return False


def is_currency_pair_exists(curr1, curr2):
    pair = f'{curr2}-{curr1}'
    if curr2 == 'KZT':
        pair = f'{curr1}-{curr2}'
    curr = currency_pairs.get(pair)
    if curr is None: 
        return False
    else: 
        return True


def add_update_currency_pair(curr1, curr2, num1, num2):
    if curr1 == 'KZT':
        currency_pairs[f'{curr2}-{curr1}'] = round(float(num1) / float(num2), 2)
    else:
        pair = f'{curr1}-{curr2}'
        currency_pairs[pair] = round(float(num2) / float(num1), 2)


def get_rate(num, currFrom, currTo):
    result = 0
    if currFrom == 'KZT':
        curr = currency_pairs.get(f'{currTo}-{currFrom}')
        result = float(num) / curr
    else:
        curr = currency_pairs.get(f'{currFrom}-{currTo}')
        result = float(num) * curr
    result = round(result, 3)
    return result


while True:
    string = input('>>> ')
    strs = string.split(' ')
    if is_currency(strs[1]) and is_currency(strs[2]) or is_currency(strs[1]) and is_currency(strs[3]):
        if is_number(strs[0]) is False:
            print('Неверное число')
            continue
        if is_currency(strs[1]) and is_currency(strs[2]):
            if is_currency_pair_exists(strs[1], strs[2]):
                result = get_rate(strs[0], strs[1], strs[2])
                print(result)
            else: 
                print('Нет такой валютной пары')
        elif is_currency(strs[1]) and is_currency(strs[3]):
            if is_number(strs[2]) is False:
                print('Неверное число')
                continue
            if is_currency_pair_exists(strs[1], strs[3]):
                add_update_currency_pair(strs[1], strs[3], strs[0], strs[2])
                print('Такая валютная пара уже существует\nКурс обновлен')
            else:
                add_update_currency_pair(strs[1], strs[3], strs[0], strs[2])
                print('Валютная пара добавлена')
    else:
        print('Неверный формат')
