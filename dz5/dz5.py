import os


path = 'C:\\'
tasks = ''


for i in os.walk(path):
    for file in i[2]:
        path_to_file = f'{i[0]}\\{file}'
        file_name, file_extension = os.path.splitext(path_to_file)
        if file_extension == '.c' or file_extension == '.cpp' or file_extension == '.cxx' or file_extension == '.cc' or file_extension == '.cs' or file_extension == '.cls' or file_extension == '.vbp': 
            with open(path_to_file) as f:
                for i, line in enumerate(f):
                    if 'TODO' in line:
                        tasks += f'{path_to_file}: #{i}, {line[line.find("TODO"):]}\n'


with open('tasks.txt', 'w') as f:
    f.write(tasks)