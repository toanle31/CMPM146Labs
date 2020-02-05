
from math import inf, sqrt
from heapq import heappop, heappush
def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = []# list of line segment (src, p1, p2,...., dst)
    boxes = []# list of boxes (src_box, b1, b2,..., dst_box)

    #path, boxes = a_star(mesh, source_point, destination_point)
    path, boxes = a_star(mesh, source_point, destination_point)

    #BFS(mesh, source_point, destination_point) #BFS call for debug

    if path and boxes:
        return path, boxes
    else:
        path = []
        boxes = []
        return path, boxes

#check if point is inside box
def point_check(box, point):
    x, y = point
    x1, x2, y1, y2 = box
    #if (this) then point is outside of box
    if (x < x1 or x > x2 or y < y1 or y > y2):
        return False
    else:
        return True

#this return box if point is in box
def search_for_box(mesh, point):
    for box in mesh['boxes']:
        if point_check(box, point):
            return box
    return False

#kept this function to test to make sure if path is possible
def BFS(mesh, source_point, destination_point):
    Q = []
    visited = []
    found = False

    src_box = search_for_box(mesh, source_point)
    dest_box = search_for_box(mesh, destination_point)

    # Makes sure both points are valid.
    if src_box and dest_box:
        pass
    else:
        print('No Path Found With BFS')
        return False, False

    Q.append(src_box)
    visited.append(src_box)
    while Q:
        current_box = heappop(Q)
        if current_box == dest_box:
            found = True
            break
        #check all adj of src
        for adj_box in mesh["adj"][current_box]:
            if adj_box not in visited:
                Q.append(adj_box)
                visited.append(adj_box)
    if not found:
        print("No Path Found With BFS!")
    else:

        print("Found path with BFS")

def get_euclidean_dist(p1, p2):
    return sqrt( ((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2) )

#if a path exist this return a dict with two lists
# one with line segments, other with boxes
def a_star(mesh, source_point, destination_point):
    Q = []

    prev_from_source = {}
    prev_from_destination = {}

    forward_dist = {}
    backward_dist = {}

    detail_points = {}

    path = []# list of line segment (((x,y),(x,y)), .....)
    boxes = []# list of boxes (src_box, b1, b2,..., dst_box)

    src_box = search_for_box(mesh, source_point)
    dest_box = search_for_box(mesh, destination_point)

    # Makes sure both points are valid.
    if src_box and dest_box:
        pass
    else:
        print('No Path Found')
        return False, False

    detail_points[src_box] = source_point
    prev_from_source[src_box] = None
    forward_dist[src_box] = 0
    source_dist_so_far = 0

    detail_points[dest_box] = destination_point
    prev_from_destination[dest_box] = None
    backward_dist[dest_box] = 0
    destination_dist_so_far = 0

    #Taking care of cases where source_point and destination_point are the same
    # and if they are in the same box
    if source_point == destination_point or src_box == dest_box:
        path.append((source_point, destination_point))
        boxes.append(src_box)
        return path, boxes

    heappush(Q, (0, src_box, 'destination'))
    heappush(Q, (0, dest_box, 'source'))

    while Q:
        priority, current_box, current_goal = heappop(Q)

        # if the goal is the destination and the path from the destination has already visited it
        if current_goal is 'destination' and current_box in prev_from_destination:
            print('Paths have met!')
            print('Meeting Point')
            print(current_box)
            print(current_goal)

            backtrace_to_source = prev_from_source[current_box]
            backtrace_to_destination = prev_from_destination[current_box]
            print('Back to Source')
            print(backtrace_to_source)
            print('Back to Destination')
            print(backtrace_to_destination)

            if backtrace_to_source is not None:
                path.insert(0, (detail_points[backtrace_to_source], detail_points[current_box]))
            if backtrace_to_destination is not None:
                path.append((detail_points[backtrace_to_destination], detail_points[current_box]))
            boxes.insert(0, current_box)

            print(path)

            while backtrace_to_source != src_box:
                print('\n Returning to Source')
                boxes.insert(0, backtrace_to_source)
                path.insert(0, (detail_points[prev_from_source[backtrace_to_source]], detail_points[backtrace_to_source]))
                backtrace_to_source = prev_from_source[backtrace_to_source]

            path.insert(0, (source_point, detail_points[backtrace_to_source]))
            boxes.insert(0, src_box)

            while backtrace_to_destination != dest_box:
                print('\n Returning to Destination')
                boxes.insert(0, backtrace_to_destination)
                path.insert(0, (detail_points[prev_from_destination[backtrace_to_destination]], detail_points[backtrace_to_destination]))
                backtrace_to_destination = prev_from_destination[backtrace_to_destination]

            path.append((destination_point, detail_points[backtrace_to_destination]))
            boxes.insert(0, dest_box)

            print(path)
            return path, boxes

        # if the goal is the source and the path from the source has already visited it
        elif current_goal is 'source' and current_box in prev_from_source:
            print('Paths have met!')
            print('Meeting Point')
            print(current_box)
            print(current_goal)

            backtrace_to_destination = prev_from_destination[current_box]
            backtrace_to_source = prev_from_source[current_box]
            print('Back to Source')
            print(backtrace_to_source)
            print('Back to Destination')
            print(backtrace_to_destination)

            if backtrace_to_source is not None:
                path.insert(0, (detail_points[backtrace_to_source], detail_points[current_box]))
            if backtrace_to_destination is not None:
                path.append((detail_points[backtrace_to_destination], detail_points[current_box]))
            boxes.insert(0, current_box)

            print(path)

            while backtrace_to_source != src_box:
                print('\n Returning to Source')
                boxes.insert(0, backtrace_to_source)
                path.insert(0, (detail_points[prev_from_source[backtrace_to_source]], detail_points[backtrace_to_source]))
                backtrace_to_source = prev_from_source[backtrace_to_source]

            path.insert(0, (source_point, detail_points[backtrace_to_source]))
            boxes.insert(0, src_box)

            while backtrace_to_destination != dest_box:
                print('\n Returning to Destination')
                boxes.insert(0, backtrace_to_destination)
                path.append((detail_points[prev_from_destination[backtrace_to_destination]], detail_points[backtrace_to_destination]))
                backtrace_to_destination = prev_from_destination[backtrace_to_destination]

            path.append((destination_point, detail_points[backtrace_to_destination]))
            boxes.insert(0, dest_box)

            print(path)
            return path, boxes

        else:
            #calculate distance to current_node
            if current_goal is 'destination' and prev_from_source[current_box] != None:
                source_dist_so_far += get_euclidean_dist(detail_points[current_box], detail_points[prev_from_source[current_box]])

            if current_goal is 'source' and prev_from_destination[current_box] != None:
                destination_dist_so_far += get_euclidean_dist(detail_points[current_box], detail_points[prev_from_destination[current_box]])

            for adj_box in mesh["adj"][current_box]:
                #[max(b1x1, b2x1), min(b1x2, b2x2), max(b1y1, b2y1), min(b1y2), b2y2]
                #border = (x1, x2, y1, y2) of border edge
                border = [max(current_box[0], adj_box[0]), min(current_box[1], adj_box[1]), max(current_box[2], adj_box[2]), min(current_box[3], adj_box[3])]
                mid_point = ((border[0] + border[1]) / 2, (border[2] + border[3]) / 2)

                dist_left = get_euclidean_dist(detail_points[current_box], (border[0], border[2]))
                dist_right = get_euclidean_dist(detail_points[current_box], (border[1], border[3]))
                dist_mid = get_euclidean_dist(detail_points[current_box], mid_point)

                if min(dist_left, dist_right, dist_mid) == dist_left:
                    adj_box_point = (border[0], border[2])
                elif min(dist_left, dist_right, dist_mid) == dist_right:
                    adj_box_point = (border[1], border[3])
                else:
                    adj_box_point = mid_point

                edge_distance = get_euclidean_dist(adj_box_point, detail_points[current_box])
                dist_remaining = get_euclidean_dist(adj_box_point, destination_point)

                #add distance traveled so far with remaining distance
                #dist_so_far going forward + edge_distance + remaining distance to destination
                if current_goal is 'destination':
                    distance = source_dist_so_far + edge_distance + dist_remaining

                    if adj_box not in forward_dist or distance < forward_dist[adj_box]:
                        forward_dist[adj_box] = distance
                        prev_from_source[adj_box] = current_box
                        detail_points[adj_box] = adj_box_point
                        heappush(Q, (distance, adj_box, 'destination'))
                else:
                    #add distance traveled so far with remaining distance
                    #dist_so_far going backward + edge_distance + remaining distance to source
                    distance = destination_dist_so_far + edge_distance + dist_remaining
                    if adj_box not in backward_dist or distance < backward_dist[adj_box]:
                        backward_dist[adj_box] = distance
                        prev_from_destination[adj_box] = current_box
                        detail_points[adj_box] = adj_box_point
                        heappush(Q, (distance, adj_box, 'source'))

    print("No Path found by A*")
    return None, None
