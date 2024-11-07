# Stories by Indigo
---
## Team Flag:
<img src="https://raw.githubusercontent.com/Stanleyhoo1/Indigo__stanleyh28_colyic_jacobl153_naomil49/main/flag.jpg" width="200"></img>
---
## Roster:

Storing and retrieving info from the databases, linking everything together, css/styling, user logins, some html templates  – Stanley\
css/styling, html pages – Jacob/Naomi\
Nothing - Colyi (disappeared)

## Description: 
This project is a collaborative storytelling website, allowing users to create and edit stories. Users must register in order to make edits or create new stories. The homepage displays all previously edited stories and created stories. The contributions page (shows up when user is logged in) displays all stories the user has contributed to. The In Progress page will display all stoires currently still in progress. The Completed page will display all completed stories. When viewing a story, the user has the option to make changes to the story if they have not previously edited it if it is not completed. After editing, they may only view the full story and cannot edit. When creating a new story, users must add a title as well. When editing, the previous edit will be displayed on top for reference, and users will have the option to complete a story, or close it to further edits. Make sure that you want that version of the story to be final and more more changes to be made. Once a story is completed, it is viewable to all users, whether or not they have contributed to it. Displayed underneath each story are its contributors in chronological order (first user made first edit, etc.)

## Install guide: how to clone/install
- Ensure that you have git installed on your computer, you don't you can install it from here: https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop
- Once you have git installed, make sure that you have set up your ssh keys correctly. If you need help, refer to this documentation: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
- Once you set up your ssh key, you are ready to clone the repository! First, open terminal or command prompt
- Navigate to the directory where you want to clone this repository
- You can clone it now by running the following command:

  ```git clone git@github.com:Stanleyhoo1/Indigo__stanleyh28_colyic_jacobl153_naomil49.git```
- You can now run our code! See the next section on how to run our app

## Launch codes: how to run
- Open terminal or command prompt if not already open
- Navigate to the cloned folder using command:
  ```cd path/to/folder```
- Install the virtual enviorment using the command:
  ```python3 -m venv foo```
- Activate the virtual environment using the command:
  ```. foo/bin/activate```
- From venv, install required packages listed in requirements.txt:
```python
pip install -r requirements.txt
```
- Naviate to the app folder using the command:
  ```cd app```
- From app, run \_\_init\_\_.py:
```
python3 __init__.py
```
- Open the link in browser to view the homepage
