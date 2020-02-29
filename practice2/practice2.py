import requests
import urllib

response = requests.get('https://google.com')
html_text = response.text

#print(html_text[5:10],html_text[:11])
link = ''
for i in range(len(html_text) + 6):
    if html_text[i:i+4] == 'http':
        #print(html_text[i:i+6])
        for j in range(len(html_text[i:])):
            if html_text[j:j+2] != '">':
                link += html_text[j]
            else:
                break
        #print('\n-------\n',link,'\n-------\n')
        link = ''