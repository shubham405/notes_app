from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,current_user
from .models import Notes
from . import db
import json
views=Blueprint('views',__name__)
@views.route('/',methods=['GET','POST'])
#@login_required is used bcz to access hoe user need to login
#current_user contains all the details of current logged in user
@login_required
def home():
    if request.method=='POST':
        notes=request.form.get('user_notes')
        if len(notes)<1:
            flash('Notes is empty',category='error')
        else:
            notes_added=Notes(data=notes,user_id=current_user.id)
            db.session.add(notes_added)
            db.session.commit()
            flash('Notes added!',category='success')
    return render_template("home.html",user=current_user,fname=current_user.first_name,lname=current_user.last_name)


@views.route('/delete-note',methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Notes.query.get(noteId)
    if note: 
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
        return jsonify({})