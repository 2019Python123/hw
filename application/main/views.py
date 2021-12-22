from flask import request,redirect,render_template,session,url_for,current_app,abort,send_from_directory,send_file,make_response
from flask_login import login_required,current_user
from . import main
from application import db
from application.models import User


@main.route("/")
def index():
    # user = User.query.filter_by(id=1).first()
    return render_template("main/index.html")


@main.route("/self_center")
@login_required
def self_center():
    return render_template("main/center.html")


@main.route("/static/<string:args>")
@login_required
def show(args):
    file_data = args.split('\\')
    type_ = file_data[0]
    print(args)
    content = None
    tem_path = ""
    path = ""
    import os.path as op
    for p in op.dirname(__file__).split("\\")[0:-1]:
        path += p + "\\"
    path += 'static\\'
    if type_ == 'img' or type_ == 'captcha':
        content = url_for('static',filename=type_+'/'+file_data[-1])
        tem_path += type_+'/'+file_data[-1]
    else:
        for p in range(len(file_data)):
            if p < len(file_data)-1:
                path += file_data[p]+'\\'
            else:
                pass
        try:
            tem_path = path+file_data[-1]
            with open(tem_path,'r',encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(e)
            return send_from_directory(directory=path, filename=args.split("\\")[-1], as_attachment=True)
    session['system_file_path'] = tem_path
    return render_template("main/pre_file.html",content=content,type=type_,path=file_data[-1])


@main.route("/download_file/<string:filename>",methods=['GET'])
@login_required
def down_file(filename):
    path = ''
    ds = session['system_file_path'].split('\\')
    for paths in range(len(ds)):
        if paths < len(ds)-1:
            path += ds[paths]+'\\'
        else:
            break;
    return send_from_directory(directory=path, filename=filename, as_attachment=True)