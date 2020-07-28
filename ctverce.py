from flask import Flask, request, render_template, redirect, session, send_from_directory
import _thread

app = Flask(__name__)
app.config.from_object(__name__)

currentLetter = "A"


@app.route("/")
def home_view():
    return f"<h1 style='font-size:50em'>{currentLetter}</h1>"


def runserver(name):
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5020)
        app.url_map.strict_slashes = False


_thread.start_new_thread(runserver, ("srv",))
# runserver()
