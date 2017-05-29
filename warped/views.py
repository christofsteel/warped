import sys
import signal
import os
import json
import argparse
from datetime import datetime

from flask import Flask, render_template, request, Response, \
    jsonify, send_file, make_response

# Initialize global variables
app = Flask(__name__)
app.mutex_groups=[]

def parse_argument(name, json, action):
    try:
        argument = json[name]
        if type(argument) == list:
            if len(argument) == 1:
                return action.type_function(argument[0])
            else:
                return [action.type_function(elem) for elem in argument]
        else:
            return action.type_function(argument)
    except (KeyError, ValueError):
        if name.endswith("[]"):
            return action.on_none
        else:
            return parse_argument(name + "[]", json, action)


@app.route("/arguments", methods=['POST'])
def fill_namespace():
    json = dict(request.form)
    namespace = argparse.Namespace()
    all_actions = app.actions

    for group in app.mutex_groups:
        all_actions.extend(group.actions)

    for action in all_actions:
        value = parse_argument(action.name, json, action)
        setattr(namespace, action.name, value)

    app.namespaceQueue.put(namespace)
    app.output.queue.put(("sig", "start"))
    return "OK"


@app.route("/arguments", methods=['GET'])
def get_arguments():
    return jsonify({'actions': [a.as_dict() for a in app.actions],
                    'groups': [g.as_dict() for g in app.mutex_groups]})


@app.route("/stop")
def stop():
    os.kill(app.module_process.pid, signal.SIGCONT)
    app.module_process.terminate()
    app.output.queue.put(("sig", "stop"))
    return "OK"

@app.route("/resume")
def resume():
    os.kill(app.module_process.pid, signal.SIGCONT)
    app.output.queue.put(("sig", "resume"))
    return "OK"

@app.route("/pause")
def pause():
    os.kill(app.module_process.pid, signal.SIGSTOP)
    app.output.queue.put(("sig", "pause"))
    return "OK"

@app.route('/clear')
def clear():
    app.output.queue.put(("sig", "clear"));
    return "OK"

@app.route("/reload")
def reload():
    if app.module_process.is_alive():
        return 403, "Process is still running"
    app.restart.set()
    app.output.queue.put(("sig", "reload"))
    return "OK"

@app.route("/download", methods=['GET'])
def download():
    output = "\n".join([line for msg_type, line in app.output.cache if msg_type != 'sig'])
    response = make_response(output)
    response.headers["Content-Disposition"] = \
        "attachment; filename=%s_%s.log" \
        % (app.name, datetime.now().strftime('%Y%m%d-%H%M%S'))
    return response


@app.route("/output.json", methods=['GET'])
def output():
    def generate():
        yield '{"output":['
        app.output.sem.acquire()
        cache = app.output.cache
        output = app.output.add_client()
        app.output.sem.release()
        for msg_type, line in cache:
            yield json.dumps({'type': msg_type, 'line': line})
            yield ','

        while not app.restart.is_set():
            msg_type, line = output.get()
            print("Send ({}): {} (length: {})".format(msg_type, line, len(line)), file=sys.__stdout__)
            yield json.dumps({'type' : msg_type, 'line': line})
            yield ','

        yield '\{\}]}'

    return Response(generate(), mimetype="application/json")



@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", mutex_groups=app.mutex_groups, actions=app.actions, name=app.name, description=app.desc)

