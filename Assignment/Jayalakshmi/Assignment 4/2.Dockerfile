FROM jobportal:latest
WORKDIR ~/Desktop/
ADD . jobportal/
WORKDIR ~/Desktop/html
RUN pip install -r requirements
RUN chmod +x app.sh
CMD ["/bin/sh","app.sh"]