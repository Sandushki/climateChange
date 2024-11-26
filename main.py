from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from images import prediction
from speech import recognize
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forums.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image', methods = ['GET', 'POST'])
def image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'no file part'
        file = request.files['file']
        if file.filename == '':
            return 'No Selected File'
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = f'static/uploads/{filename}'
            class_name = prediction(file_url)
            return render_template('image.html', filename=filename, class_name=class_name)
        
    return render_template('image.html')

@app.route('/forums')
def forums():
    posts = Forum.query.order_by(Forum.id).all()

    return render_template('forums.html', posts=posts)

@app.route('/create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        text =  request.form['text']

        post = Forum(title=title, text=text)

        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')    

@app.route('/record')
def record():
    text = recognize()
    return render_template('create.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)