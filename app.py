from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///members.db"
db = SQLAlchemy(app)

class Member(db.Model):
	__tablename__ = "Member"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	cg = db.Column(db.String(20))

	def __init__(self, name, cg):
		self.name = name
		self.cg = cg

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/sheep")
def sheep():
	result = Member.query.all()
	return render_template("success.html", result=result)	

@app.route("/register", methods=["POST"])
def register():
    if request.form["name"]=="" or request.form["cg"]=="":
        return render_template("failure.html")
    else:    
    	sheep = Member(request.form["name"], request.form["cg"])
    	db.session.add(sheep)
    	db.session.commit()
    	result = Member.query.all()
    	return render_template("success.html", result=result)

@app.route("/unregister", methods=["GET", "POST"])
def unregister():
	if request.method == "GET":
		result = Member.query.all()
		return render_template("unregister.html", result=result)
	elif request.method == "POST":
		Member.query.filter(Member.id == request.form["id"]).delete()
		db.session.commit()
	return redirect(url_for("sheep"))

@app.route("/update", methods=["GET", "POST"])
def update():
	if request.method == "GET":
		result = Member.query.all()
		return render_template("update.html", result=result)
	elif request.method == "POST":
		update = Member.query.filter(Member.id == request.form["id"]).first()
	return render_template("updating.html", update=update)

@app.route("/updating", methods=["POST"])
def updating():
	update = Member.query.filter(Member.id == request.form["id"]).first()
	update.name = request.form["name"]
	update.cg = request.form["cg"]
	db.session.commit()
	return redirect(url_for("sheep"))



if __name__ == '__main__':
	app.run(debug=True)	