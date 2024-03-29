from flask import Flask, request

from df_engine.core import Context, Actor
from df_engine.core.keywords import TRANSITIONS, RESPONSE
from df_engine import conditions as cnd
from df_engine import responses as rsp

from dff_db_connector import connector_factory

plot = {
    "greeting_flow": {
        "start_node": {  # This is an initial node, it doesn't need a `RESPONSE`
            RESPONSE: "",
            TRANSITIONS: {"node1": cnd.exact_match("Hi")},  # If "Hi" == request of user then we make the transition
        },
        "node1": {
            RESPONSE: rsp.choice(["Hi, what is up?", "Hello, how are you?"]),  # random choice from candicate list
            TRANSITIONS: {"node2": cnd.exact_match("alright")},
        },
        "node2": {
            RESPONSE: "Good. What do you want to talk about?",
            TRANSITIONS: {"node3": cnd.exact_match("Let's talk about music.")},
        },
        "node3": {
            RESPONSE: "Sorry, I can not talk about that now.",
            TRANSITIONS: {"node4": cnd.exact_match("Ok, goodbye.")},
        },
        "node4": {RESPONSE: "bye", TRANSITIONS: {"node1": cnd.exact_match("Hi")}},
        "fallback_node": {  # We get to this node if an error occurred while the agent was running
            RESPONSE: "Oops",
            TRANSITIONS: {"node1": cnd.exact_match("Hi")},
        },
    }
}

app = Flask(__name__)

connector = connector_factory("json://file.json")

actor = Actor(plot, start_label=("greeting_flow", "start_node"), fallback_label=("greeting_flow", "fallback_node"))


@app.route("/chat", methods=["GET", "POST"])
def respond():
    user_id = str(request.values.get("id"))
    user_message = str(request.values.get("message"))
    context = connector.get(user_id, Context(id=user_id))

    context.add_request(user_message)
    updated_context = actor(context)
    response = updated_context.last_response

    updated_context.clear(hold_last_n_indexes=3)
    connector[user_id] = updated_context
    return {"response": str(response)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
