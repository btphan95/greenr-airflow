sudo apt-get install nginx -y
sudo cp config/default-airflow /etc/nginx/sites-enabled/default
sudo nginx -s reload

