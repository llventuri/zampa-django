# ZAMPA PROJECT
redeploy step by step instructions:

```
cd /home/ubuntu/djangozampa
docker stop zampa-django
docker rm zampa-django
git pull
docker build -t zampa-django:0.1 .
docker run -d -p 8080:8080 -v /var/www/zampa.online:/var/www/zampa.online --name zampa-django zampa-django:0.1
docker exec -it zampa-django python manage.py collectstatic
```

