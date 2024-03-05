FROM python:3

WORKDIR /usr/src/app

EXPOSE 7860

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./* /usr/src/app/

ARG USER_API_KEY=default
ENV OPENAI_API_KEY=${USER_API_KEY}

CMD [ "python", "app.py" ]
