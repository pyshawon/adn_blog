# Simple Django Blog
For ADN Diginet Ltd.


### Installation & Run

```bash
# Clone the repo.
$ git clone https://github.com/pyshawon/adn_blog.git 

# Navigate to adn_blog
$ cd adn_blog

# Create Virtual ENV.
$ virtualenv -p python3 venv

# Activate Virtual ENV.
$ source venv/bin/activate

# Install Requirements
$ pip install -r requirements.txt

# Navigate to src folder
$ cd src

# Run Database migrations
$ python manage.py migrate

#To Create Superuser
$ python manage.py createsuperuser

# Run Tests
$ python manage.py test

# Run Server
$ python manage.py runserver


```


### PERSONAL NOTES (TODO)
- Write more test case.
- Some Query Optimization
- Use Cache Server (Redis)
- More.




### THANK YOU