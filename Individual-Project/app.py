from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={"apiKey": "AIzaSyB5vbNNlRb29MTo7KyprTtaks8nqih_uJ4",
  "authDomain": "mini-cs-project-7bc38.firebaseapp.com",
  "databaseURL": "https://mini-cs-project-7bc38-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "mini-cs-project-7bc38",
  "storageBucket": "mini-cs-project-7bc38.appspot.com",
  "messagingSenderId": "96839359364",
  "appId": "1:96839359364:web:3af9b39245bbc641d11bd1",
  "databaseURL":"https://mini-cs-project-7bc38-default-rtdb.europe-west1.firebasedatabase.app/"}

results = {"brunet":
{"cold"         :{"winter":["darkblue","blue","darkgreen"],"summer":["green","turquise"],"spring":["darkpink","darkpurple"],"autumn":["can't predict"]},
"hot"           :{"winter":["can't predict"],"summer":["orange","bordo"],"spring":["pink","magenta"],"autumn":["beige","mustard yellow"]},
"light_cold"    :{"winter":["pastel blue","grey"],"summer":["blond"],"spring":["pastel purple","pastel pink"],"autumn":["can't predict"]},
"light_hot"     :{"winter":["can't predict"],"summer":["peach"],"spring":["can't predict"],"autumn":["rose gold"]}},

"blond":
{"cold"         :{"winter":["black"],"summer":["strawberry blond"],"spring":["purple"],"autumn":["can't predict"]},
"hot"           :{"winter":["can't predict"],"summer":["green"],"spring":["light brown"],"autumn":["orange"]},
"light_cold"    :{"winter":["light blue"],"summer":["pastel green"],"spring":["pastel cyan"],"autumn":["can't predict"]},
"light_hot"     :{"winter":["can't predict"],"summer":["lime green"],"spring":["fiusha"],"autumn":["muted red"]}},

"black":
{"cold"         :{"winter":["white","dark blue"],"summer":["can't predict"],"spring":["purple"],"autumn":["can't predict"]},
"hot"           :{"winter":["can't predict"],"summer":["yellow"],"spring":["saturated green"],"autumn":["red"]},
"light_cold"    :{"winter":["platinum blond","icy blond (blue-ish)"],"summer":["can't predict"],"spring":["light violet"],"autumn":["can't predict"]},
"light_hot"     :{"winter":["can't predict"],"summer":["darkgreen"],"spring":["can't predict"],"autumn":["peach"]}},


"ginger":
{"cold"         :{"winter":["blue"],"summer":["turquoise"],"spring":["purple","violet"],"autumn":["muted red"]},
"hot"           :{"winter":["can't predict"],"summer":["pastel yellow-orange"],"spring":["violet"],"autumn":[" warm blond"]},
"light_cold"    :{"winter":["pastel blue"],"summer":["can't predict"],"spring":["pastel turquoise"],"autumn":["can't predict"]},
"light_hot"     :{"winter":["can't predict"],"summer":[" pastel yellow"],"spring":["olive green"],"autumn":["golden yellow"]}},


"light_brown":
{"cold"         :{"winter":["pastel navy"],"summer":["can't predict"],"spring":["seafoam"],"autumn":["can't predict"]},
"hot"           :{"winter":["can't predict"],"summer":["red"],"spring":["can't predict"],"autumn":["Darker brown"]},
"light_cold"    :{"winter":["grey blond"],"summer":["can't predict"],"spring":["pastel green"],"autumn":["can't predict"]},
"light_hot"     :{"winter":["can't predict"],"summer":["chartreuse"],"spring":["can't predict"],"autumn":["golden"]}},

"colored":
{"cold"         :{"winter":"too colored","summer":"too colored","spring":"too colored","autumn":"too colored"},
"hot"           :{"winter":"too colored","summer":"too colored","spring":"too colored","autumn":"too colored"},
"light_cold"    :{"winter":"too colored","summer":"too colored","spring":"too colored","autumn":"too colored"},
"light_hot"     :{"winter":"too colored","summer":"too colored","spring":"too colored","autumn":"too colored"}}
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route("/",methods=['GET', 'POST'])
def login ():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            login_session["user"]=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for("user_page"))
        except Exception as e:
            print(e)  
            error="Authentication failed"   
    return render_template("login.html")


@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        username = request.form['username']
        try:
            login_session["user"]= auth.create_user_with_email_and_password(email,password)
            UID = login_session["user"]["localId"]
            user = {"email": email,"username":username,"password":password}
            db.child("Users").child(UID).set(user)
            return redirect(url_for("ques"))
        except Exception as e:
            print(e)
    return render_template("signup.html")


@app.route("/ques",methods=['GET','POST'])
def ques():
    if request.method=="POST":
        try:
            color = request.form['color']
            new_color = request.form['new_color']
            season = request.form['season']
            
            login_session["results"]=results[color][new_color][season]

            return redirect(url_for("display_results"))
        except:
           return render_template("ques.html")
    return render_template("ques.html")


@app.route("/results",methods=['GET','POST'])
def display_results():
    if request.method=="POST":
        try:
            res={"result":login_session["results"]}
            UID = login_session["user"]["localId"]
            db.child("Users").child(UID).child("results").push(res)
            return redirect(url_for("user_page"))
        except Exception as e:
            print(e)
    else:
        print(login_session["results"])
    return render_template("results.html", results = login_session["results"])


@app.route("/user_page",methods=['GET','POST'])
def user_page():
    UID = login_session['user']['localId']
    username = db.child("Users").child(UID).get().val()['username']
    return render_template("user_page.html", username=username)


@app.route("/reco",methods=['GET','POST'])
def recommendations():
    UID = login_session["user"]["localId"]
    users = db.child('Users').child(UID).child('results').get().val()
    return render_template("recommendations.html",Users=users)


# @app.route("/posts",methods=['GET','POST'])
# def posts():
#     if request.method=="POST":
#         try:
#             desc=request.form["title"]
#             post=request.form["your_photo"]
#             print()
#             upost={"posts":post,"desc":desc}
#             UID = login_session["user"]["localId"]
#             db.child("Users").child(UID).child("posts").push(upost)
#             return redirect(url_for("user_page"))
#         except:
#             print("bbbbbb")
    
#     return render_template("post.html")

@app.route('/logout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('login'))



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)