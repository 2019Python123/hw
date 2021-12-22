import os
from random import randint

def get_file(path):
    dirs = os.listdir(path)
    index = randint(0,len(dirs))

    return (path.split("/"))[2]+"/"+dirs[index],(dirs[index].split("."))[0]


def img_to_base64(file,file_type=""):
    import base64
    data = base64.b64encode(file)
    print("data:image/"+file_type+";base64,"+data.decode("utf-8"))
    return "data:image/"+file_type+";base64,"+data.decode("utf-8")


def split_name(names):
    names = names.replace(' ','').split(",")
    strings = []
    for name in names:
        name = name.split("\n")
        strings.append(name[0:3])
    return strings


if __name__ == '__main__':
    with open("static/img/favicon.ico", 'rb') as f:
        img_to_base64(f.read())
    print(get_file("./static/captcha"))