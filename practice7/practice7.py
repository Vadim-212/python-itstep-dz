import re


string = """
валидные домены: a.b.c, -d-9--.1foo-bar2-.lolipop, ftp://d-9.1foo-bar2.lolipop/index.php, a.b1.co, LOL1.FOO-bar.COM.
невалидные домены: abc.a_d.com, com..kz, .com.kz,  ab.do.-com
"""


pattern = r'(?<!\.)\b(?!-)[A-z0-9-]+\.(?!-)[A-z0-9-]+\.(?!-)[A-z]{1,}\b(?!\.\S)'
print('findall:', re.findall(pattern, string))
