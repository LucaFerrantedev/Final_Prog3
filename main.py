from flask import Flask, render_template, request, redirect, session, send_from_directory
from business.logic import checkUserPass
from business.dataset import procesar_dataset
import os
import dotenv

dotenv.load_dotenv()
app = Flask(__name__, template_folder="./templates")
app.secret_key = os.getenv("COOKIES_SECRET_KEY")

@app.route("/", methods=['GET', 'POST'])
def index():
    error = False
    if request.method == 'GET':
        return render_template("login.html", error=error)
    if request.method == 'POST':
        user = request.form["username"]
        pwd = request.form["password"]
        if checkUserPass(user, pwd):
            session['logged_in'] = True
            session['user'] = user
            return redirect("/welcome")
        else:
            error = True
            return render_template("login.html", error=error)

@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    try:
        if not session.get('logged_in'):
            return redirect("/")

        welcomeText = session['user']
        plot_url = None
        r_squared = None
        error_msg = None
        
        # Si se envía el archivo CSV
        if request.method == 'POST':
            if 'csv_file' in request.files:
                file = request.files['csv_file']
                if file.filename != '':
                    try:
                        # Llamada a la función con el nombre actualizado
                        plot_url, r_squared = procesar_dataset(file)
                    except Exception as e:
                        error_msg = f"Error al procesar: {str(e)}"

        return render_template("welcome.html", welcomeText=welcomeText, plot_url=plot_url, r_squared=r_squared, error_msg=error_msg)

    except KeyError:
        return redirect("/")

@app.route("/logout", methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect("/")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)