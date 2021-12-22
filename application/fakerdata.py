from faker import  Faker
from application.models import *
from application import db
from application import app_factory

fake = Faker("zh_CN")
def faker():
    for i in range(30):
        p = Post(title=fake.sentence(4),body=fake.text(2000),author_name='曾思龙',author_id=1,species_id=6)
        db.session.add(p)
    db.session.commit()


def speices():
    sp = ['java','python','c++|c','c#','安卓','前端']

    for i in range(len(sp)):
        s = Species(name=sp[i])
        db.session.add(s)
        db.session.commit()


if __name__ == '__main__':
    with app_factory().app_context():

        faker()