from flask_admin import BaseView,expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask import url_for,redirect,current_app,render_template,request,flash,jsonify
from flask_login import current_user,login_required
from .forms import PostForm
from . import admin_bp
import json
from application.helper import split_name


class PostsView(BaseView):
    @expose("/")
    def show_posts(self):
        return self.render("admin/posts.html")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class ExitView(BaseView):
    @expose("/")
    def return_index(self):
        """
        返回到首页
        :return:
        """
        return redirect(url_for('main.index'))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class UserView(BaseView):
    @expose("/")
    def user_(self):
        pass

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class UserCoreView(BaseView):
    @expose("/")
    def return_core(self):
        """
        返回到个人中心页面
        :return:
        """
        return redirect(url_for("main.self_center"))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class UserLogoutView(BaseView):
    @expose("/")
    def return_logout(self):
        """
        退出登录
        :return:
        """
        return redirect(url_for("auth.logout"))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class CreateHomeWorkView(BaseView):
    """
    发布作业视图类
    """
    @expose("/")
    def create_home_work(self):
        """
        创建作业
        :return:
        """
        return redirect(url_for("createhomeworkview.new_homework"))

    @expose("/new/",methods=['POST','GET'])
    def new_homework(self):
        """
        以博客的方式创建作业
        :return:
        """
        form= PostForm()
        if form.validate_on_submit():
            from application.models import Homework,Species,HomeWork_Author
            from application import db
            sp = Species.query.filter_by(id=int(form.categories.data)).first()
            home = Homework(title=form.title.data,
                            body=form.text.data,
                            author_id=current_user.id,
                            author_name=current_user.name,
                            describe=form.describe.data,
                            species_id=int(form.categories.data),
                            species_name=sp.name,
                            difficulty=form.difficulty.data
                            )


            try:
                db.session.add(home)
                db.session.commit()
                home_ = Homework.query.filter_by(author_name=current_user.name)\
                    .order_by(Homework.timestmp.desc()).first()
                home_user = HomeWork_Author(author_id=current_user.id,homework_id=home_.id)
                db.session.add(home_user)
                db.session.commit()
                flash("发布一条作业")
            except Exception as e:
                print(e)
                db.session.rollback()
            return redirect(url_for("createhomeworkview.create_home_work"))
        return self.render("admin/edit_homework.html", form=form)

    @expose("/new/file",methods=['POST','GET'])
    def release_file(self):
        """
        以文件的形式发布作业
        :param: request.files['file'] 接受前端传来的作业文件，文件格式为  作业标题-难度[0-11]-标签[java/python]-作业描述
        :return:
        """
        diff = ['炼气','筑基','旋照','融合','心动','灵寂','元婴','出窍','分神','合体','度劫','大乘','渡劫']
        # 接受文件
        file = request.files['file']
        print(file.filename)
        import os.path as op
        print(op.dirname(__file__))
        path = ''
        # 获取当前路径
        ops = op.dirname(__file__).split("\\")
        for p in range(len(ops)):
            if p < len(ops) - 1:
                path += ops[p] + '\\'
            else:
                pass
        # 最终字符拼接的路径为 static\\release_work
        path += 'static\\release_work\\'
        # 保存文件
        file.save(path + file.filename)
        # 分离文件名
        names = file.filename.split("-")
        from application.models import Homework,HomeWork_Author,Species
        from application import db
        sp = Species.query.filter_by(name=names[-2]).first()
        # 将作业存储到数据库中
        home = Homework(title=names[0],
                        body= file.filename,
                        author_id=current_user.id,
                        author_name=current_user.name,
                        describe=names[-1],
                        species_id=sp.id,
                        species_name=names[-2],
                        difficulty=diff[int(names[1])],
                        is_url = True
                        )
        try:
            db.session.add(home)
            db.session.commit()
            # 将作者与作业进行关联，提交到作业布置记录表中
            home_ = Homework.query.filter_by(author_name=current_user.name) \
                .order_by(Homework.timestmp.desc()).first()
            h_a = HomeWork_Author(
                homework_id=home_.id,
                author_id=current_user.id,
                author_name = current_user.name
            )
            db.session.add(h_a)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return jsonify({'code':200})

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class ReleaseHomeWorkView(BaseView):
    """
    布置作业视图类
    """
    @expose("/")
    def to_release_html(self):
        """
        返回布置作业页面
        :return:
        """
        from application.models import Homework,User
        homeworks = Homework.query.all()
        users = User.query.all()
        return self.render("admin/release_hoemwork.html",homeworks=homeworks,users=users)

    @expose("/release",methods=['POST','GET'])
    def release(self):
        """
        进行发布作业
        :return:
        """
        from application.models import HomeWork_User,User
        from application import db
        data = request.get_data(as_text=True)
        data = json.loads(data)
        # 获取布置作业的对象姓名
        owner_list = split_name(data['names'])
        # 未布置该作业的对象字符串
        names = ''
        # 已经布置了该作业的对象字符串
        names_ed = ''
        # 用户id列表
        ids = []
        # 作业所属者列表
        for owner in owner_list:
            try:
                # 循环查询数据库获取每个User对象
                user = User.query.filter_by(name=owner[0]).first()
                # 创建 作业-用户 关联对象，每一分作业对应一个所属者
                hw = HomeWork_User.query.filter_by(owner_id=user.id,homework_id=data['work_id']).first()
                # 如果这个关联对象不存在数据库，证明这个作业没有对该用户进行布置
                if hw is None:
                    # 新建一个关联对象
                    hw = HomeWork_User(homework_id=data['work_id'],owner_id=user.id,owner_name=user.name,publish_name=current_user.name)
                    db.session.add(hw)
                    db.session.commit()
                    names += user.name+' '
                    # 将用户id添加到列表中
                    ids.append(user.id)
                else:
                    names_ed += user.name + ' '
            except:
                db.session.rollback()
                return jsonify({'msg':'没有选择对象,布置任务失败'})
        msg = ''
        if names != '':
            msg +='已经给'+names+'布置任务成功'
        if names_ed != '':
            msg +=' 已经给%s布置了任务' %(names_ed)
        return jsonify({'code':200,'msg':msg,'users':ids,'sender_id':current_user.id})

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))



