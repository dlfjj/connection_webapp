# IntroductionsManagerWebsite
A website to make introductions with linkedin contacts easier. 

Welcome!

This is the repository for all the code used to create the Introductions Management Website, a django-based app to help folks find the contacts they need to make introductions to people on linkedin. 

This is not a finished product at it's current stage; it is more aptly described as a PoC that looks nice :)

**To-Do:**
  - Support more complex queries
  - Host on AWS and DNS config
  - Use an Apache HTTP (rather than the built in django server, which is not suitable for production)
  - Create a user login interface to avoid constantly having to type in linkedin usernames/passwords with every search

**Requirements/Dependencies:**
  - Python 3.x with the default pip3
  - virtualenv running the following: 
    - Django 1.11 (pip install)
    - Selenium (pip install)
    - Google Chrome Driver

**Quickstart Guide for Developers:**
For dev purposes, we use virtualenv to run django. Virtualenv will create a folder you specify (e.g. 'environment1') with the following subdirectories: 
  - bin
  - include
  - lib
Create another subfolder called UCM (Short for Unshackled Contacts Manager) and insert this repo into that folder. Add in the google chrome driver (!!!see note below!!!), and you're ready to activate the virtual env!

Open your favorite terminal-like program, change directories to the virtual enviroment you created. Activate the virtual environment (i.e. source bin/activate). Use 'pip install ____' to install the required packages, and now you should have a fully functioning django environment!

Now let's change directories to the subdirectory UCM. Notice that this directory has a script called manage.py -- don't touch it! DO NOT TOUCH ANYTHING when you are unaware of the consequences! This manage.py is your friend in doing a lot of things. Let's start by testing to see if we can run the server and have it start listening for requests:

python manage.py runserver

This runs the default django server (not apache or nginx or anything fancy. This needs to be updated). Navigate to http://localhost:8000/intros/query/ and you should see a beautiful query homepage! Check out the UCM/IntroManagers/urls.py to see what other urls (besides intros/query) will point to live pages. Enjoy!


**Structure:**
UCM
-- \__pycache\__ (don't touch)
-- connectionsGrabber.py
-- IntroManger
  -- \__init\__.py
  -- \__pycache\__
  -- admin.py
  -- apps.py
  -- migrations
    -- \__init\__.py
    -- \__pycache\__
    -- 0001_initial.py
    -- ... (for each migration it creates something like 0002_something.py)
  -- models.py
  -- static
    -- IntroManager
      -- images
        -- background.jpg
      -- style.css
      -- UVCLogo.png
  -- templates (*clean this up!*)
    -- IntroManager
    -- registration
      -- base.html
      -- login.html
    -- signup
  -- tests.py
  -- urls.py
  -- views.py
-- manage.py
-- UCM
  -- \__init\__.py
  -- \__pycache\__
  -- settings.py
  -- urls.py
  -- wsgi.py

Most of the things you touch as a developer will be in UCM/IntroManager (static, templates, tests.py, urls.py, views.py) or UCM/UCM (settings.py, urls.py).

The basic gist of this is easy. If you want to make a page, follow these steps:
1. Define a url that will point to your page in either UCM/UCM/urls.py (i.e. domain/urlchosen) or UCM/IntroManager/urls.py (i.e. domain/intros/urlchosen).
2. Link that url to a "view" you specify in UCM/IntroManager/views.py
3. Link the view to an HTML page you specify in UCM/IntroManager/templates/IntroManager
4. Style that HTML with a css file in UCM/IntroManager/static/IntroManager


*Note that in connectionsGrabber.py I set an absolute path to the chrome driver -- oops... You should change that path to point to the location of the driver in your setup and knock me on the head three times for this annoyance (Sorry!). In the future, make sure to make this a relative path so that it's no longer an issue on new setups.* 
