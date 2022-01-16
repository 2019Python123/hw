FROM python:3.6
WORKDIR /home/admin/hw

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "manage:app", "-c", "./gunicorn.conf.py"]