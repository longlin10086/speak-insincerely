FROM python:3

WORKDIR /usr/src/speak-insincerely

EXPOSE 7860

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/speak-insincerely/


CMD [ "python", "app.py" ]
