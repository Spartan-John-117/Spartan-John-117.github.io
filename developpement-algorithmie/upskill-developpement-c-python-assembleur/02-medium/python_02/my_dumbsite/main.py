from flask import Flask, render_template, redirect
from formulaire import MyForm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from model.model import Account, Base


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'P4ssw0rd'

engine = create_engine(f'sqlite:///model/logins.db')
Base.metadata.create_all(engine)

@app.route("/")
def root_page():
    return render_template ('main_page.html')

@app.route("/add_user", methods=('GET', 'POST'))
def add_user():
    form = MyForm()
    if form.validate_on_submit():
        # Connexion à la base de données
        session = Session(engine)
        
        # Collecte des données soumises
        recv_data = {}
        for d in vars(form):
            if d != 'csrf_token' and d != 'submit' and hasattr(getattr(form, d), 'data'):
                recv_data[d] = getattr(getattr(form, d), 'data')
        
        # Crée une nouvelle entrée dans le modèle Account
        acc = Account(**recv_data)
        session.add(acc)
        session.commit()
        
        return redirect('/list_user')
    return render_template ('add_user.html', form=form)

@app.route("/list_user")
def list_user():
    session = Session(engine)

    users = session.query(Account).all()

    session.close()
    return render_template("list_user.html", users=users)

@app.route("/show_user/<int:one_id>")
def show_user(one_id):
    session = Session(engine)

    user = session.query(Account).filter_by(id=one_id).first()

    session.close()
    if user:
        return render_template('show_user.html', user=user)

    else:
        return "Utilisateur inconnu", 404

if __name__ == "__main__":
    # forever serve
    app.run(port=5000)
