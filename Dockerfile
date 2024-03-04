FROM python:3

WORKDIR /usr/src/app

EXPOSE 7860

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "sh", "-c", "env.sh"]
CMD [ "python", "./app.py" ]
