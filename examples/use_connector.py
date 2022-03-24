from flask import Flask

from df_engine.core import Context, Actor
from df_engine.core.keywords import TRANSITIONS, RESPONSE
from df_engine import conditions as cnd

from dff_db_connector import JsonConnector

plot = {
    "root": {
        "start": {RESPONSE: "Hi", TRANSITIONS: {("root", "hello"): cnd.true()}},
        "fallback": {RESPONSE: "Bye", TRANSITIONS: {("root", "start"): cnd.true()}},
        "hello": {RESPONSE: "Long time no see", TRANSITIONS: {("root", "fallback"): cnd.true()}},
    }
}

app = Flask(__name__)

connector = JsonConnector("json://file.json")

actor = Actor(plot, start_label=("root", "start"), fallback_label=("root", "fallback"))


@app.route("/chat", methods=["POST"])
def respond():
    user_id = str(request.form["id"])
    context = connector.get(user_id, Context(id=user_id))

    updated_context = actor(context)

    updated_context.clear(hold_last_n_indexes=3)
    connector[user_id] = updated_context
    return {"response": updated_context.last_response}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
