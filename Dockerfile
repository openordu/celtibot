from registry.access.redhat.com/ubi8/python-38:latest
ENV ACCESS_TOKEN="yourtoken"
ENV SERVER="https://yourendpoint/api"
ENV MODE=information
ENV DRYRUN=1
ENV BOT_ACCOUNT_ID=000000000000000000
USER 0
RUN mkdir -p /tmp/bot
WORKDIR /tmp/bot
ADD . .
RUN /usr/bin/fix-permissions /tmp/bot
USER 1001
WORKDIR /tmp/bot
RUN /usr/bin/pip3 install --user -r requirements.txt
ENTRYPOINT /usr/bin/python3 /tmp/bot/src/celtibot.py --mode ${MODE} --dryrun ${DRYRUN}