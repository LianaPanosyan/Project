import os
import time
import json
import requests
import threading

print('*********')
json_name = input('Enter your json file name.>>> ')
print('*********')
dir_name = input('Pleas enter your directory name for downloading pictures.>>> ')

t1 = time.time()

pic_names = []
urls_list = []
thread_list = []

try:
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, dir_name) 
    os.mkdir(path)

    with open(json_name, 'r') as f:
        data = json.load(f)
    for i in data.values():
        for j in i:
            a = list(j.values())[0]
            urls_list.append(a)

    for i in range(1, len(urls_list) + 1):
        name = 'picture_' + str(i) + '.jpeg'
        pic_names.append(name)

except FileExistsError:
    print('*********')
    print('Folder with the same name already exists.')

def download_images(url, name):
    try:
        r = requests.get(url)
        out = open(f'{path}/{name}', 'wb')
        out.write(r.content)
        out.close()
        print(f'{name} downloaded !')
    except requests.exceptions.RequestException as e:
        print('Somthing went wrong with URLs.')

for i in range(0, len(urls_list)):
    t = threading.Thread(target = download_images, args = (urls_list[i], pic_names[i]))
    thread_list.append(t)
    t.start()
for j in thread_list:
    j.join()

t2 = time.time()

print('*********')
print(f'The program ends in {t2 - t1} seconds.')

if os.path.exists(path) and len(os.listdir(path)) == 0:
    print(f'Folder {dir_name} deleted because it is empty.')
    os.rmdir(path)
