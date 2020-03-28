from collections import namedtuple
from random import sample
symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
employees_info = []
emp = namedtuple('Employee',('full_name','id','position','login','password'))

with open('info.txt', 'r') as f:
    lines = f.read().split('\n')
    for line in lines:
        employees = line.split(':')
        full_name = f'{employees[1][0]}. {employees[2][0]}. {employees[3]}'
        new_login = (employees[1][0] + employees[2][0] + employees[3]).lower()
        new_password = ''.join(sample(symbols,8))
        employees_info.append(emp(full_name = full_name, id = employees[0], position = employees[4], login = new_login, password = new_password))

with open('out.html','w') as f:
    f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Employees info</title></head><body><table><thead><tr><th>Full name</th><th>Id</th><th>Position</th><th>Login</th><th>Password</th></tr></thead><tbody>')
    for i, e in enumerate(employees_info):
        f.write(f'<tr><td>{e.full_name}</td><td>{e.id}</td><td>{e.position}</td><td>{e.login}</td><td>{e.password}</td></tr>')
    f.write('</tbody></table><style>td, th {padding: 5px 15px;}table, td, th{border: 1px solid black;}</style></body></html>')