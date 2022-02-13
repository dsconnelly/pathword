import flask

from game import Pathword

app = flask.Flask(__name__)
game = Pathword('words.txt')

@app.route('/')
def index():
    game.start_new_game()

    return flask.render_template(
        'index.html',
        start=game.start,
        end=game.end
    )

@app.route('/validate', methods=['POST'])
def validate():
    curr = flask.request.json['curr']
    next = flask.request.json['next']

    try:
        game.validate(curr, next)
        return flask.jsonify({'success' : True})
    except ValueError as error:
        return flask.jsonify({
            'success' : False,
            'message' : str(error)
        })

@app.route('/path', methods=['POST'])
def path():
    return flask.jsonify({
        'path' : game.path
    })

if __name__ == '__main__':
    app.run()
