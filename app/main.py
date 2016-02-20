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

    # Find head
    for snake in data['snakes']:
        if snake['id'] == id:
            head = snake['coords'][0]

    # Initialize, then build 'bad locs' list
    for x in range(0,width):
        for y in range(0, height):
            occupied[x][y] = False
    for snake in data['snakes']:
        for coord in snake['coords']:
            occupied[coord[0]][coord[1]] = True

    posMoves = {'north': False, 'east': False, 'south': False, 'west': False}

    # Go north>
    if head[1] -1 >= 0 and not occupied[head[0]][head[1]-1]:
        posMoves['north'] = True
    # Go east?
    if head[0] +1 < data['width'] and not occupied[head[0]+1][head[1]]:
        posMoves['east'] = True
    # Go south?
    if head[1] +1 < data['height'] and not occupied[head[0]][head[1]+1]:
        posMoves['south'] = True
    # Go west?
    if head[0] -1 >= 0 and not occupied[head[0]-1][head[1]]:
        posMoves['west'] = True

    for move in posMoves:
        if posMoves[move]:
            decision = move

    if data['turn'] == 0:
        decision = 0

    elif data['turn'] == 1:
        decision = 1

    else:
        decision = 2

    # return statements
    if decision == 'north':
        return {
            'move': 'north',
        }
    if decision == 'east':
        return {
            'move': 'east',
        }
    if decision == 'south':
        return {
            'move': 'south',
        }
    if decision == 'west':
        return {
            'move': 'west',
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
