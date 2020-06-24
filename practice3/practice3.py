latin = ['a','b','v','g','d','e','jo','zh','z','i','j','k','l','m','n','o','p','r','s','t','u','f','h','c','ch','sh','shh','','y','\'','je','yu','ya']
cyrillic = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

def cyrillicToLatin(string):
    new_string = ''
    for i, c in enumerate(string):
        try:
            if c.isupper():
                new_string += latin[cyrillic.index(c.lower())].upper()
            else:
                new_string += latin[cyrillic.index(c)]
        except ValueError:
            new_string += c
    return new_string

def latinToCyrillic(string):
    string += '   '
    new_string = ''
    i = 0
    while i <= len(string) - 3:
        symbols3 = string[i]+string[i+1]+string[i+2]
        symbols2 = string[i]+string[i+1]
        try:
            if symbols3.isupper():
                new_string += cyrillic[latin.index(symbols3.lower())].upper()
            else:
                new_string += cyrillic[latin.index(symbols3)]
            i += 3
        except ValueError:
            try:
                if symbols2.isupper():
                    new_string += cyrillic[latin.index(symbols2.lower())].upper()
                else:
                    new_string += cyrillic[latin.index(symbols2)]
                i += 2
            except ValueError:
                try:
                    if string[i].isupper():
                        new_string += cyrillic[latin.index(string[i].lower())].upper()
                    else:
                        new_string += cyrillic[latin.index(string[i])]
                    i += 1
                except ValueError:
                    new_string += string[i]
                    i += 1
    return new_string


example_string = 'привет МИР, это Python'
print('1. '+example_string)
example_string = cyrillicToLatin(example_string)
print('2. '+example_string)
example_string = latinToCyrillic(example_string)
print('3. '+example_string)