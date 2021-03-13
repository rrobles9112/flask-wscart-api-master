# flask-wscart-api 

REST API for a webshop cart. The API implement a handler for saving and fetching shopping cart data to and from a database. 


## Technologies used
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[MySQL](https://www.mysql.com/downloads/)** – [Why MySQL?](https://www.mysql.com/why-mysql/).
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/msubair/flask-wscart-api.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd flask-wscart-api
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 venv
        $ pip install autoenv
        ```

* #### Environment Variables
    Create a .env file and add the following:
    ```
    source venv/bin/activate
    export FLASK_APP="run.py"
    export FLASK_APP_SETTINGS="development"
    export FLASK_SECRET="this is random string secret"
    export MYSQL_USER="<change with your mysql username>"
    export MYSQL_PASSWORD="<change with your mysql password>"
    export MYSQL_DATABASE_NAME="WSCartAPI"
    ```

    Save the file. CD out of the directory and back in.

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

* #### Migrations
    On your MySQL console, create your main database (for development/production):
    ```
    > CREATE DATABASE WSCartAPI;
    ```
    Also for testing, create special test databasase:
    ```
    > CREATE DATABASE test_WSCartAPI;
    ```
    Then, make and apply your Migrations (if you not change anything, you can directly to db upgrade). If you want to create your own initiate upgrade, then:
    ```
    (venv)$ rm -rf migrations

    (venv)$ python manage.py db init

    (venv)$ python manage.py db migrate
    ```

    And finally upgrade, migrate your migrations to persist on the DB
    ```
    (venv)$ python manage.py db upgrade
    ```

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ flask run
    ```
    Or if you want to define address/port, you can
    ```
    (venv)$ flask run --host=0.0.0.0 --port=5000
    ```
    You can now access the app on your local browser (after login) by using CURL or REST client 
