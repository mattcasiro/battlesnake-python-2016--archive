import bottle

id = "9b1c136b-6edb-43d5-a265-8f528136a608"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#ffffff',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    print (data)

    return {
        'taunt': 'Full Monty Baby'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    for snake in data['snakes']:
        if snake.id == id:
            head = snake.coords[0]
            print "head at: {}, {}" .format(head[0], head[1])
            break

    return {
        'move': 'north',
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'You got STRIPPED'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080)
