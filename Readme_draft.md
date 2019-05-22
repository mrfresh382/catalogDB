# Catalog App Project
Submitted by Doug McDonald for Udacity Full Stack Nanodegree.
I submitted the files directly, but kept versions on GitHub for backup and future work to implement a project portfolio. This is a website for a fictional general store at the Big Bend National Park.

## System Specs
- Python 2.7.13, Vagrant 2.2.2, VirtualBox 5.2.2
- System Specs: Windows 7, 64 bit
- Used GitBash as the terminal, Windows Powershell 5.1
- Used VM provided "OAuth" Ubuntu 16.04
- Code checked with PEP8 'pycodestyle'

## Getting Started
### Prerequisites 
A Google account and GitHub account are required for this project to have full permissions for CRUD on the webpage. A unique client secret token is required to operate the login and logout page. The login.html file will need to be updated prior to running the project for full functionality. Some knowledge of Python 2 library, Flask, and Jinja is required to manipulate the Python , HTML, and CSS files. *** I included some Javascript /JQuery also.

### Setup
I used the Udacity provided 'OAuth' VM for this project. It can be cloned from the OAuth course on Github @ 'github.com/udacity/OAuth2.0' Please follow the instructions on this lesson to install the VM. A shell is needed to operate this app. 

1. Use GitBash Shell and `cd` to the vagrant directory 
2. Start VM- `vagrant up`. This will instantiate the Ubuntu VM. The CLI messages will indicate a successful load. This takes several minutes the first time.
3. Install Flask, Oauth2Client, HttpLib2, Requests and any other python packages on the VM. `sudo pip install python-oauth2client` and `sudo pip install python-flask`.etc... You can run the python files and debug errors or try to run the `import Library` command in a Python 2 shell to test if they are installed on your VM. 
4. Goto http://console.developers.google.com and login to your Google Account. Create a Credentials instance within the Google API & Services section. You will need the *name*,  *Client ID* and the *Client Secrets JSON file*. The name used here is 'Catalog App' ( use this to reduce overhead work). Create the OAUTH 2.0 Client and copy/paste the Name and Client ID into a text file for later use. In the edit section, download the JSON file and save to the Vagrant folder in the VM. Rename as 'client_secrets.json' to match with the code in this app. Then include your local host :
- http://localhost:5000
...in the section "Authorized Javascript Origins" . Also include :
- http://localhost:5000
- http://localhost:5000/gconnect
- http://localhost:5000/gdisconnect
- http://localhost:5000/login
... in the section 'Authorized Redirect URIs'. The OAUTH client will not work without these. 
- Note: If you reset the client secret, you have to repeat the above steps, otherwise OAuth will not work.

5. Update Login.HTML - Line 9 needs to updated with YOUR Client_ID. Overwrite the Client_ID and save the file. Steps 4 and 5 are very important, so read them in their entirety before beginning work. 

6. Ensure your Vagrant folder has the following files at a minimum before proceeding: 
	- catalog-app.py 
	- catalogDBpreLOAD.py
	- catalogDB_setup.py
	- client_secrets.json 
	- Static Folder- styles.css , blank-user.gif, and top-banner.jpeg
	- Template Folder- 

6. The existing python files will not work with the filesystem on Windows computers. After research on the Udacity Knowledge forum and StackOverflow, I had to perform this one-time conversion to ensure there were no errors on execution. Install the app 'Dos2Unix' on the VM `sudo apt-get install dos2unix`. Then cd into the vagrant directory with the 3 python files. Execute `dos2unix catalog-app.py` and `dos2unix ...` for the other 2 files. There should be no errors. If you have a different VM, then you may need to troubleshoot the 'shebang' line for each file prior to running the app.
 
### User Guide for Udacity Grader and General Public

1. Use shell and cd to the vagrant directory 
2. Open VM- `vagrant up`
3. SSH into VM- `vagrant ssh`
4. Once SSHed into VM type `cd /vagrant`
5. From this folder you can run the project files, Static, and Template folder. Check to ensure they are accessible by executing `ls` command. If they are not viewable, check that you are in the '/vagrant' folder, then proceed with troubleshooting. 
6. Execute python file within VM `python catalogDB_setup.py`. This will establish a blank SQLite database for the web app. 
7. (Optional) Execute `python catalogDBpreLOAD.py` . This will add some info in the database for testing and viewing in the webpage. 
8. Execute `python catalog-app.py` This will start the web app on port 5000 on your local machine. Visit http://localhost:5000 on either Firefox or Chrome to view the home page. Some output messages are visible on the shell. To close App, enter 'CTRL-C' on the keyboard to terminate.
9. (Optional) For more advanced debug, open a seperate shell and use NCAT to view all HTTP requests. 
```
ncat -l 5000
```

## Notes/Issues/Bugs
- I had to update Virtual Box and Windows Management Framework 5.1 A.k.a. Powershell 5.1.
- In Sublime, I had to change the 'Tabs' to 'Spaces', this cleared out the numerous PEP warnings. 
- Google OAuth does not work with Microsoft Internet Explorer for me. However, the webapp works in public mode. I did not have time to troubleshot this issue. Please post a solution on GitHub or explore the web for a solution. 
- Ensure you have a **graceful shutdown** of vagrant instance before you shutdown or restart your OS. Use command `vagrant halt` to prevent corrupting the news database and vagrant instance. Despite this, the Vagrant instance seemed to occasionally get corrupt. 

## Design Notes
### GUI
I decided to "Love" the framework provided by Udacity and make some minor tweaks to the HTML layout and CSS. I made GUI updates throughout the project, while constantly testing for functionality. I added Login and Logout links in the appropriate places. Then I ensured that site navigation was functional. 

### OAuth
The first thing I did was follow along with the lessons and work to get my OAuth login and logout working.

### Catalog DB
I refactored the database_setup.py file from the lesson to create catalogDB_setup.py. Each category is a section of the store. Each item, is an item sold at the store. I then created catalogDBpreLOAD.py to load dummy data into the database for additional testing. I tested by using 2 different Google accounts to ensure CRUD functions worked as desired. 

### JQuery and Drop Down lists
I added JQuery to the Main page so that the user can preview category items before clicking on each category individually. 

## Built With
- Sublime Text

## Author
[mrfresh382](https://github.com/mrfresh382)

## Acknowledgments
Much of the OAuth functionality was provided by Lorenzo Brown and the Udacity staff. Udacity's code can be found in the lessons and on [GitHub](https://github.com/udacity/OAuth2.0)