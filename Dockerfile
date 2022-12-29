from registry.access.redhat.com/ubi8/python-38:latest
ENV ACCESS_TOKEN=${ACCESS_TOKEN:-"yourtoken"}
ENV SERVER=${SERVER:-"https://yourendpoint/api"}
ENV MODE=information
ENV DRYRUN=1
USER 0
RUN mkdir -p /tmp/bot
WORKDIR /tmp/bot
ADD . .
RUN /usr/bin/fix-permissions /tmp/bot
USER 1001
WORKDIR /tmp/bot
RUN /usr/bin/pip3 install --user -r requirements.txt
ENTRYPOINT /usr/bin/python3 /tmp/bot/src/celtibot.py --mode ${MODE} --dryrun ${DRYRUN}