# Flask Reservation App Template for PythonAnywhere Hosting
This is a Flask reservation app template designed for hosting on [PythonAnywhere](https://www.pythonanywhere.com). It serves as a full-stack application to demonstrate the understanding and ability to perform all aspects of full-stack web app development in Python, from template creation to deployment.

### Create virtual environment in local machine
> python -m venv venv

### Initiate venv in local machine
> venv source/bin/activate

### Create virtual environment in pythonanywhere
> mkvirtualenv venv --python=/usr/bin/python3.10

### VENV path in pythonanywhere
/home/username/.virtualenvs/venv

### Intiate venv in pythonanywhere
> workon venv

### Requirements
> pip install -r requirements.txt

### Deactivate VENV
> deactivate

## Navbar and Page Navigation
Navbar options for menu and overall static site navigation are configured in `my_config.py`. Ensure that all static pages you wish to navigate to are defined in the `ALLOWED_PAGES`.

## Additional Pages & Routers for Complex Apps

1 - If a page requires interaction with a router (typical for complex apps), create the routers in `index.py`.

2 - All static pages used in the application must be registered in the `ALLOWED_PAGES` list within `my_config.py`. Failing to register a page will result in 404 Error.

## Creating New Pages
1 - Create an HTML file within the `templates/pages/` directory.

2 - Use `templates/pages/main.html` as an example of how to correctly extend `layout.html`.




