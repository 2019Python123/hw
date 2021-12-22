from flask_admin.contrib.sqla import  ModelView
from flask_login import current_user
from flask import  request,redirect,url_for
from jinja2 import Markup


class UsersView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_export = True
    can_view_details = True
    column_labels = dict(
        id='id',
        name='昵称',
        email = '邮箱',
        sex = '性别',
        img_data='头像',
        zhuanye = '专业',
        main_='主修',
        fuxiu_='辅修',
        about_me = '个性签名',
        role_id='角色id',
        timestmp = '记录提交时间'
    )
    column_exclude_list = (
        'passwd_hash'
    )
    column_searchable_list = ['name', 'email','zhuanye','sex','role_id']
    column_filters = ['sex','zhuanye','role_id']

    def _avatar(self, context, model, name):
        return Markup('<img src="%s" alt="" style="width: 50px; height: 50px">' % (model.img_data))

    def _man_or_woman(self,context,model,name):
        return Markup("<label class='label label-primary'>%s</label>" % (model.sex)) \
            if model.sex == "男" \
            else Markup("<label class='label label-danger'>%s</label>" % (model.sex))

    def _name(self,context,model,name):
        return Markup("<span style='color: green'>%s</span>" %(model.name))

    def _learn(self,context,model,name):
        return Markup("<span class='label label-info'>%s</span>" %(model.main_))

    column_formatters = { 'img_data': _avatar,'sex':_man_or_woman,'name':_name}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class PostView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        title='标题',
        body = '内容',
        author_name = '作者',
        author_id = '作者id',
        species_id = '标签id',
        timestmp = '记录提交时间'
    )
    column_exclude_list = (

    )

    def _content(self,context, model, name):
        return Markup("<a class='label label-info' href='%s'>%s</a>" %(url_for('blog.show_post',page_id=model.id),"查看详情"))

    column_searchable_list = ['author_name', 'title','species_id']
    column_filters = ['species_id','author_name']
    column_formatters = {'body':_content}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class RoleView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        role_name='角色名',
        default='是否为默认角色',
        permission='权限值',
        timestmp = '记录提交时间'
    )
    column_exclude_list = (

    )

    def _label_role(self,context, model, name):
        return Markup("<label class='label label-primary'>%s</label>" %(model.role_name)) \
            if model.role_name != "Administrator" \
            else Markup("<label class='label label-danger'>%s</label>" %(model.role_name))

    column_formatters = {'role_name':_label_role}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class SpeciesView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        name='标签名',
        timestmp = '记录提交时间'
    )
    column_exclude_list = (

    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class HomeWorkView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        title='标题',
        body='内容',
        describe='作业内容描述',
        species_name='作业标签',
        species_id='标签id',
        author_id='作者id',
        author_name='作者',
        difficulty='难度',
        timestmp = '记录提交时间'
    )
    column_exclude_list = (

    )

    def _content(self,context, model, name):
        return Markup("<a class='label label-info' href='%s'>%s</a>" %(url_for('blog.show_work_admin',works_id=model.id),"查看详情"))

    column_searchable_list = ['author_name', 'title','species_name']
    column_filters = ['species_name','author_name','difficulty']
    column_formatters = {'body':_content}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class HomeWork_UserView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        homework_id='作业id',
        owner_id='作业所属者id',
        owner_name='发布的作业对象',
        publish_name='布置作业者',
        is_complete='完成情况',
        timestmp='记录提交时间'
    )
    column_exclude_list = (

    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class HomeWork_AuthorView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        homework_id='作业id',
        author_id='作业创建者id',
        timestmp='记录提交时间'
    )
    column_exclude_list = (

    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class Submit_LogView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        homework_id='作业id',
        author_id='提交作业者id',
        submiter_name='提交作业者',
        answer='提交答案',
        timestmp='记录提交时间'
    )
    column_exclude_list = (

    )

    def _content(self, context, model, name):
        url = None
        if model.answer.find("ht")!=-1:
            id = model.answer.split('/')[-1]
            url = url_for('blog.show_post', page_id=int(id))
        else:
            path = ''
            op = model.answer.split('\\')
            path = op[-2]+'\\'+op[-1]
            url = url_for('main.show',args=path)
        return Markup("<a class='label label-info' href='%s'>%s</a>" % (url, model.answer))

    column_formatters = {'answer':_content}
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))


class MessageView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_set_page_size = 10
    can_view_details = True
    can_export = True
    column_labels = dict(
        sender_id='发送者id',
        accept_id='接受者id',
        body='消息内容',
        is_read = '阅读情况',
        timestmp='消息提交时间'
    )
    column_exclude_list = (

    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 6

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))