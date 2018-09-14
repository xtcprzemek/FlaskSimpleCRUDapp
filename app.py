import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import func



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        #id = Book.query(func.max(id))+1
        id=db.session.query(db.func.max(Book.id)).scalar()+1
        book = Book( id =id , title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()

    books = Book.query.all()

    maxi = db.session.query(db.func.max(Book.id)).scalar()
    cnt = db.session.query(db.func.count(Book.id)).scalar()
    return render_template("home.html", books=books, max=maxi, cnt=cnt)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")



@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)

