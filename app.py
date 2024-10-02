from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myanimes.db'
db = SQLAlchemy(app)

# Define the anime model
class Animes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    movie_list = Animes.query.all()
    return render_template('index.html', movie_item=movie_list)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        image = request.form.get('image')
        
        # Create new anime entry
        new_movie = Animes(title=title, genre=genre, image=image)
        
        # Add to the database
        db.session.add(new_movie)
        db.session.commit()
        
        # Redirect to home page after adding
        return redirect(url_for('index'))
        
    return render_template('add_movie.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
