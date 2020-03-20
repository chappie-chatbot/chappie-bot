FROM python:3.7

ENV HOME /app

RUN pip install rasa

ADD ./entrypoint.sh /entrypoint.sh

WORKDIR $HOME

#RUN useradd -d $HOME rasa && chown -R rasa $HOME

#USER rasa

ENTRYPOINT ["/entrypoint.sh"]
