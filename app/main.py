import bottle
import math
import os

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
        'color': '#c3756e',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    print (data)

    return {
        'taunt': 'GET IN MAH BELLY'
    }
def dist(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

@bottle.post('/move')
def move():
    data = bottle.request.json

    # Find head
    for snake in data['snakes']:
        if snake['id'] == id:
            head = snake['coords'][0]
            ourLength = len(snake['coords'])

    #TO DO REMOVE DEAD SNAKES
    occupied = []
    for x in range(0,data['width']):
        occupied.append([])
        for y in range(0, data['height']):
            occupied[x].append(False)

    for snake in data['snakes']:
        # if len(snake['coords']) >= ourLength and snake['id'] != id:
        #     if snake['coords'][0][0] + 1 >= data['width']:
        #         occupied[snake['coords'][0][0] + 1][snake['coords'][0][1]] = True
        #     if snake['coords'][0][0] - 1 < 0:
        #         occupied[snake['coords'][0][0] - 1][snake['coords'][0][1]] = True
        #     if snake['coords'][0][1] + 1 >= data['height']:
        #         occupied[snake['coords'][0][0]][snake['coords'][0][1] + 1] = True
        #     if snake['coords'][0][1] - 1 < 0:
        #         occupied[snake['coords'][0][0]][snake['coords'][0][1] - 1] = True
        for coord in snake['coords']:
            occupied[coord[0]][coord[1]] = True

    posMoves = {'north': False, 'east': False, 'south': False, 'west': False}

    #who is the closest
    whoFood = []
    #how far
    distFood =[]
    # for foodAt in data['food']:
    #     distFood.append(dist(head,foodAt))
    #     distFood.append("0")
    #     minDist = 100000
    #     for snake in data['snake']:
    #         if dist(snake['coords'][0],foodAt) <= minDist:
    #             minDist = dist(snake['coords'][0],foodAt)
    #             whoFood[-1] = snake['id']
    #             if snake['id'] == id:
    #                 whoFood = 'me'
    # food to me
    bestFood = [-1,-1]
    acceptableFood = False

    while not acceptableFood: 
        acceptableFood = True
        minDist = 100000;
        foodIndex = 0
        for food in data['food']:
            if dist(head, food) < minDist:
                minDist = dist(head, food)
                bestFood = food
        for snake in data['snakes']:
            if snake['id'] == id:
                continue
            minDist = 100000;
            for food in data['food']:
                if dist(snake['coords'][0], food) < minDist:
                    minDist = dist(snake['coords'][0], food)
                    theirFood = food
            if theirFood == bestFood:
                if bestFood == [8,8] or [-1,-1]:
                    break
                else:
                    bestfood = data['food'][len(data['food'] - 1)]
                    break



    want = [bestFood[0] - head[0], bestFood[1] - head[1]]


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
            break

    if want[0] < 0 and posMoves['west']:
        decision = 'west'
    elif want[0] > 0 and posMoves['east']:
        decision = 'east'
    elif want[1] < 0 and posMoves['north']:
        decision = 'north'
    elif want[1] > 0 and posMoves['south']:
        decision = 'south'

    for snake in data['snakes']:
        if snake['id'] == "f729b53e-3477-447d-b07e-c79d7e326c82":
            print "Food target: {}" .format(bestFood)
            print "Head: {}" .format(head)
            print "posMoves: {}" .format(posMoves)
            print "x diff: {}" .format(want[0])
            print "y diff: {}" .format(want[1])
            print "Setting decision to {}" .format(move)


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
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
