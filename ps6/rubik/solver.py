import rubik

def shortest_path(start, end):
    if start == end:
        return []
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    travelled_dict_forward = {}
    travelled_dict_backward = {}

    #Dictionary contains (parent, previous_move)
    travelled_dict_forward[start] = None
    travelled_dict_backward[end] = None

    to_travel_list_forward = [start]
    to_travel_list_backward = [end]

    alternator = 0
    middle_node = None

    while middle_node is None:
        if alternator > 14:
            return None
        print "level " + str(alternator + 1)
        if alternator % 2 == 0:
            temp_travel_list_forward = []
            for node in to_travel_list_forward:
                move_counter = 0
                for perm in map(lambda x: rubik.perm_apply(x, node), rubik.quarter_twists):
                    if perm in travelled_dict_backward:
                        travelled_dict_forward[perm] = (node, rubik.quarter_twists[move_counter])
                        middle_node = perm
                        break
                    elif perm in travelled_dict_forward:
                        pass
                    else:
                        travelled_dict_forward[perm] = (node, rubik.quarter_twists[move_counter])
                        temp_travel_list_forward.append(perm)
                    move_counter += 1
            to_travel_list_forward = temp_travel_list_forward
            alternator += 1
        else:
            temp_travel_list_backward = []
            for node in to_travel_list_backward:
                move_counter = 0
                for perm in map(lambda x: rubik.perm_apply(x, node), rubik.quarter_twists):
                    if perm in travelled_dict_forward:
                        travelled_dict_backward[perm] = (node, rubik.perm_inverse(rubik.quarter_twists[move_counter]))
                        middle_node = perm
                        break
                    elif perm in travelled_dict_backward:
                        pass
                    else:
                        travelled_dict_backward[perm] = (node,
                            rubik.perm_inverse(rubik.quarter_twists[move_counter]))
                        temp_travel_list_backward.append(perm)
                    move_counter += 1
            to_travel_list_backward = temp_travel_list_backward
            alternator += 1
    end_cur_node = middle_node
    start_cur_node = middle_node
    start_stack = []
    while travelled_dict_forward[start_cur_node] is not None:
        start_stack.append(travelled_dict_forward[start_cur_node][1])
        start_cur_node = travelled_dict_forward[start_cur_node][0]
    start_stack.reverse()
    while travelled_dict_backward[end_cur_node] is not None:
        start_stack.append(travelled_dict_backward[end_cur_node][1])
        end_cur_node = travelled_dict_backward[end_cur_node][0]
    print(start_stack)
    return start_stack






