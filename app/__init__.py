# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: 7

from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import create_user, login_user, logout_user, create_story, create_edit, get_stories, can_add_to_story, add_to_story

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

# Home route
@app.route('/')
def home():
    content = display_stories()
    
    if 'username' in session:
        username = session['username']
        return render_template('home.html', content=content, username=username)
    return render_template('home.html', content=content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        create_user()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user()
    return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

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
    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        flash('You must be logged in to add to a story!', 'error')
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            story_id = request.form.get('data-id')
            add = can_add_to_story(story_id)
            if add:
                edit_story(story_id)
                return render_template('edit.html')
            else:
                flash('You have already edited this story!', 'error')
                return redirect(url_for('home'))

def edit_story(story_id):
    session['story_id'] = story_id  # Store story_id in the session

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        flash('You must be logged in to add to a story!', 'error')
        return redirect(url_for('home'))
    else:
        story_id = session.get('story_id')  # Retrieve story_id from session
        if request.method == 'POST':
            added = add_to_story(story_id)  # Pass story_id to the function
            if added:
                flash('You have successfully added to the story!', 'success')
                session.pop('story_id', None)
                return redirect(url_for('home'))
            else:
                flash('You have already edited this story!', 'error')
                return redirect(url_for('home'))
        return render_template('edit.html', story_id=story_id)
    
def display_stories():
    pairs, edits, user_edits = get_stories()
    # print(pairs, edits, user_edits)
    text = ''''''
    for pair in pairs:
        text += '<div style="background-color: #fffbf6;'
        text += 'padding: 5px 10px 10px 10px;'
        text += 'border-radius: 15px;'
        text += '">'
        title, story_id = pair
        if story_id in user_edits:
            story_text = ""
            counter = 1
            for edit in edits[story_id]:
                story_text += f'<p>Edit {counter}: <br>{edit}</p>\n'
                counter += 1
        else:
            story_text = edits[story_id][-1]
            last_edit = len(edits[story_id])
            
        text += f'<h3>{title}</h3>\n'
        if story_id in user_edits:
            text += f'<p>{story_text}</p>\n'
        else:
            text += f'<p>Edit {last_edit}: <br>{story_text}</p>\n'
        text += '\n<br>\n'
        text += f'''
        <form action="{url_for('edit')}" method="POST">
            <button type="submit" class="add-btn" name="data-id" value={story_id}>Add to Story</button>
        </form>
        '''
        text += '</div>'
        text += '\n<br>'
    return text

if __name__ == "__main__":
    app.run(debug=True)
