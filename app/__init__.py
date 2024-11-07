# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: 12

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import create_user, login_user, logout_user, create_story, create_edit, get_stories, can_add_to_story, add_to_story, get_contributors

# Auto-generated secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user()
    return redirect(url_for('home'))

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

# Create route
@app.route('/create', methods=['GET', 'POST'])
def create_new():
    if 'username' not in session:
        flash('You must be logged in to create a story!', 'error')
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            created = create_story()
            if created:
                return redirect(url_for('home'))
        return render_template('create_story.html')

# Edit route (verifying if they can edit)
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        flash('You must be logged in to add to a story!', 'error')
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            # Gets stored info
            story_id = request.form.get('story_id')
            previous_edit = request.form.get('previous_edit')
            # Line breaks for text
            while '\n' in previous_edit:
                previous_edit = previous_edit.replace('\n', '<br><br>')
            add, completed = can_add_to_story(story_id)
            # Checks if story is closed
            if completed == True:
                flash('Story is closed to new edits! It is complete!', 'error')
                return redirect(url_for('home'))
            # Checks if user can add to the story (ie. they already edited it)
            elif add:
                edit_story(story_id, previous_edit)
                return render_template('edit.html', story_id=story_id, previous_edit=previous_edit)
            # They can make edits
            else:
                flash('You have already edited this story!', 'error')
                return redirect(url_for('home'))

# Function to store the edited story info in the session so it doesn't lose the info when reloading
def edit_story(story_id, previous_edit):
    session['story_id'] = story_id  # Store story_id in the session
    session['previous_edit'] = previous_edit

# Route to add edits (actual edit)
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Redirects to home if not logged in (maybe they saved think somewhere to access)
    if 'username' not in session:
        flash('You must be logged in to add to a story!', 'error')
        return redirect(url_for('home'))
    else:
        story_id = session.get('story_id')  # Retrieve story_id from session
        if request.method == 'POST':
            completed = True if 'toggleComplete' in request.form else False
            added = add_to_story(story_id, completed)  # Pass story_id to the function
            if added:
                flash('You have successfully added to the story!', 'success')
                session.pop('story_id', None)
                return redirect(url_for('home'))
            else:
                flash('You have already edited this story!', 'error')
                return redirect(url_for('home'))
        return render_template('edit.html', story_id=story_id, previous_edit=previous_edit)


# Creates the html that will display the stories on the webpage
def display_stories(info_type):
    pairs, edits, user_edits = get_stories(info_type)
    text = ''''''
    # Goes though every single returned story
    for pair in pairs:
        text += '<div style="background-color: #fffbf6;'
        text += 'padding: 5px 10px 10px 10px;'
        text += 'border-radius: 15px;'
        text += '">'
        title, story_id, completed = pair
        
        # Contributors list
        contributor_list = get_contributors(story_id)
        contributors = ""
        for i in contributor_list:
            contributors += i + ", "
        contributors = contributors[:-2]
        
        # Displays full story
        if story_id in user_edits or completed == True:
            story_text = ""
            counter = 1
            for edit in edits[story_id]:
                original = edit
                while '\n' in edit:
                    edit = edit.replace('\n', '<br><br>')
                story_text += f'<p>{edit}</p>\n'
                counter += 1
        # Preview of story
        else:
            story_text = edits[story_id][-1]
            last_edit = len(edits[story_id])
            original = story_text
            # New line for all new lines otherwise its all 1 line
            while '\n' in story_text:
                story_text = story_text.replace('\n', '<br><br>')
            
        # Story title
        text += f'<h3>Title: {title}</h3>\n'
        # Story status
        status = 'Completed' if completed == True else 'In progress'
        text += f'<b>Status: {status}</b>\n'
        # Actual story
        if story_id in user_edits or completed == True:
            text += f'<p>{story_text}</p>\n'
        else:
            text += f'<p><b>Previous contribution: </b><br><br>{story_text}</p>\n'
        text += f'<p><b>Contributors:</b> {contributors}</p>'
        # If story in progress display the add to story button below
        if completed != True:
            text += f'''
            <form action="{ url_for('edit') }" method="POST">
            
                <!-- Hidden inputs for story_id and story_text -->
                <input type="hidden" name="story_id" value="{ story_id }">
                <textarea name="previous_edit" style="display:none;">{ original }</textarea>

                <!-- Submit button to add to story -->
                <button type="submit" class="add-btn">Add to Story</button>
            </form>
            '''
        text += '</div>'
        text += '\n<br>'
    return text

# Main Page Routes

# Home route
@app.route('/')
def home():
    content = display_stories(0)
    if 'username' in session:
        username = session['username']
        return render_template('home.html', content=content, username=username)
    return render_template('home.html', content=content)

# In progress route
@app.route('/in-progress')
def progress():
    content = display_stories(1)
    if 'username' in session:
        username = session['username']
        return render_template('in-progress.html', content=content, username=username)
    return render_template('in-progress.html', content=content)

# Contributions route
@app.route('/contributions')
def contributions():
    content = display_stories(2)
    if 'username' in session:
        username = session['username']
        return render_template('contributions.html', content=content, username=username)
    return render_template('contributions.html', content=content)

# Completed route
@app.route('/completed')
def completed():
    content = display_stories(3)
    if 'username' in session:
        username = session['username']
        return render_template('completed.html', content=content, username=username)
    return render_template('completed.html', content=content)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        create_user()
        return redirect(url_for('home'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
