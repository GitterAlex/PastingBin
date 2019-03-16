# PastingBin by Sam Campbell and Steven Reddy	 									     
Secure Software Assignment 2. This isn't actively hosted, the database login and other credentials are simply samples provided, you can edit them accordingly to your own database credentials.
The premise of this project is to create a simplified pastebin clone. You will need to install the following:
- pip install django
- pip install django-fernet-fields
- Some form of email server for password reset
Run with the following command:
- python .\manage.py runserver_plus --cert certname

## Main functionality
### Visitor
- Greeted with a homepage
	- Able to create an account
	- Able to login
	- Able to view any public posts by shortened URL
### Admin page
- Allows "staff" users to be able to manage users
  - Create, Delete, Edit users
  - Search function to search for posts
### Users page
- Given a dashboard
  - 10 Recent posts are displayed
  - User's own posts are displayed
  - Clicking on any post title brings user to viewing/editing
- Users can create new posts
  - Share posts (Ctrl + Click to select)
  - Restrict post access
  - Delete their posts
