import keyword
def is_symbols(string):
    symbols = ['-','.',',','/','\\','|','[',']','{','}','(',')',':',';','!','@','#','$','%','^','&','*','?','~','+','=','\'','"']
    for i in range(len(string)):
        if string[i] in symbols:
            return True
    return False

while True:
    identificator = input('>>> ')
    if identificator[0].isdigit():
        print('NOT OK: начинается с цифры')
    elif keyword.iskeyword(identificator):
        print('NOT OK: ключевое слово')
    elif is_symbols(identificator):
        print('NOT OK: содержит символы')
    elif identificator[:2] == '__':
        print('OK: так называют приватные идентификаторы')
    elif identificator[0] == '_' and identificator[1] != '_':
        print('OK: так называют защищенные идентификаторы')
    elif identificator.isupper() and '_' in identificator or identificator.isupper():
        print('OK: так называют константы')
    elif identificator[0].isupper() and '_' not in identificator:
        print('OK: так называют классы')
    elif identificator.islower() and '_' in identificator:
        print('OK: так называют переменные')
    else:
        print('OK: так называют переменные')