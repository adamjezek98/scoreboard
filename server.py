from flask import Flask, request, render_template, redirect, session, send_from_directory
import logic as lc

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def home_view():
    return render_template("home.html")


@app.route("/score")
def score_view():
    logic = lc.Logic()
    return render_template("score.html", data=logic.get_table_editable())


@app.route("/edit")
def score_editor():
    logic = lc.Logic()
    return render_template("edit.html", data=logic.get_table_editable())


@app.route("/score-edit")
def score_edit():
    logic = lc.Logic()
    return render_template("score_edit.html", data=lbogic.get_table_editable())


@app.route("/messages")
def messages_view():
    logic = lc.Logic()
    return render_template("messages.html", messages=logic.get_messages())


@app.route("/processedit")
def edit():
    logic = lc.Logic()
    logic.process_edit(request.args.getlist("id")[0], request.args.getlist("value")[0])
    return ""


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)
    app.url_map.strict_slashes = False
