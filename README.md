# btalk-api

### Steps to install the API server
1. Clone the repository.
2. Download the **.env** from Notion Docs.
3. Make a virtual environment using 
    ```
    python3 -m venv venv
    ```
4. Activate the virtual environment using 
    ```
    source venv/bin/activate
    ```
5. Install the dependencies using 
    ```
    pip install -r requirements.txt
    ```
6. Migration of the database using 
    ```
    export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
    python manage.py migrate
    ```
7. Run the server using 
    ```
    python manage.py runserver
    ```
8. Run the celery in another terminal
    ```
    celery -A btalk worker -l info
    ```

---
Restarting the Server app
```
sudo systemctl restart btalk
sudo systemctl status btalk
sudo service btalk-celery-worker restart
```
   
gunicorn --bind 0.0.0.0:8000 myproject.asgi -w 4 -k uvicorn.workers.UvicornWorker# btalk-backup
