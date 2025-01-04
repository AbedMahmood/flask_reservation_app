# my_config.py
class Config:
    WEBSITE_NAME = 'Startup'
    YEAR = 2024
    DATA_FILE = 'data.json'
    ALLOWED_PAGES = ['error', 'home', 'contact']
    NAVIGATION_ITEMS = [
        ('/home', 'Home'),
        ('/reserve', 'Reserve'),
        ('/reservations', 'Reservations')
    ]
    RESERVATION_TYPES = [
        ('orientation', 'Orientation'),
        ('resume_help', 'Resume Help'),
        ('computer_skills', 'Computer Skills'),
        ('skills_in_demand', 'Skills in Demand'),
        ('web_development', 'Web Development'),
        ('networking', 'Networking'),
    ]

