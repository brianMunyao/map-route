from queue import Empty, PriorityQueue, Queue
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut


TOWNS = ('Nairobi', 'Mombasa', 'Kisumu',
         'Eldoret', 'Kitui', 'Makueni', 'Nakuru', 'Nanyuki', 'Kilifi', 'Garissa')


def getCoordForList(cities):
    _dict = dict()
    print('Getting town data...')
    for city in cities:
        _dict[city] = getCoord(city)
        print(city)

    return _dict


def getCoord(loc):
    return recurrCoord(loc, attempt=1)


def recurrCoord(loc, attempt):
    try:
        geolocator = Nominatim(user_agent='assignment')
        location = geolocator.geocode(loc)
        return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        if attempt <= 5:
            return recurrCoord(loc, attempt+1)
        raise


def getDistance(pt1, pt2):
    return geodesic(getCoord(pt1), getCoord(pt2)).km


def getPathDistance(list):
    total = 0
    for i in range(len(list)-1):
        dist = getDistance(list[i], list[i+1])
        total = total + dist

    return int(total)


def getPath(graph, start, goal, algorithm):
    route = []
    if algorithm == 'Depth First Search':
        route = depth_first_seach(graph, start, goal)
    elif algorithm == 'Breadth First Search':
        route = breadth_first_search(graph, start, goal)
    else:
        route = aStarSearch(graph, start, goal)

    return route


def getCoordPath(townDict, route):
    res = []
    for i in route:
        res.append(townDict[i])
    return res


def clear(q):
    while not q.empty():
        try:
            q.get(False)
        except Empty:
            continue
        q.task_done()


def depth_first_seach(graph, startNode, goalNode):
    stack = [startNode]
    closedList = set()

    res = []

    while len(stack) != 0:
        curr = stack.pop()

        if curr not in closedList:
            res.append(curr)
            closedList.add(curr)

            if curr == goalNode:
                break

        for neighbor in graph.getNodes()[curr].getEdges():
            nn = neighbor.getConnections().getId()
            if nn not in closedList:
                stack.append(nn)
    return res


def breadth_first_search(graph, startNode, goalNode):
    closedList = set()
    queue = Queue()
    route = []

    queue.put(startNode)
    closedList.add(startNode)

    if startNode == goalNode:
        route.append(queue.get())

    while not queue.empty():
        curr = queue.get()
        route.append(curr)

        for neighbor in graph.getNodes()[curr].getEdges():
            nn = neighbor.getConnections().getId()
            if nn not in closedList:
                closedList.add(nn)
                if nn == goalNode:
                    clear(queue)
                    route.append(nn)
                    break
                queue.put(nn)

    return route


def aStarSearch(graph, start, goal):
    pQueue = PriorityQueue()
    closedList = set()
    route = []

    pQueue.put((0, start))

    while not pQueue.empty():
        curr = pQueue.get()[-1]
        closedList.add(curr)
        route.append(curr)

        if curr == goal:
            clear(pQueue)
            break

        neighbours = graph.getNodes()[curr].getEdges()
        for node in neighbours:
            nn = node.getConnections().getId()

            g = cost(start, nn)
            h = heuristic(nn, goal)
            f = g+h

            if nn == goal:
                route.append(nn)
                clear(pQueue)
                break
            if nn not in closedList:
                pQueue.put((f, nn))

    return route


def heuristic(curr, goal):
    # to get the cost h(n) from current node to goal node
    return getDistance(goal, curr)


def cost(start, goal):
    # to get the cost g(n) from start node to the current node
    return getDistance(goal, start)
