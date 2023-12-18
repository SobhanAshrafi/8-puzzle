


# goal state
goal = [[1,2,3],[4,5,6],[7,8,0]]

# start state
start = [[2,5,7],[4,1,3],[0,6,8]]

# curr state
curr = []

h = 0



def find_index_item_in_goal(item):

    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if goal[i][j]==item:
                return i , j


def cal_h(state):

    result = 0
    for i in range(len(state)):
        for j in range(len(state[i])):

            it = state[i][j]

            k , z = find_index_item_in_goal(it)

            result += abs(k - i) + abs(z - j)


    return result



def find_best_adj():

    new_h = h
    null_it = (0,0)



    for i in range(len(curr)):
        for j in range(len(curr[i])):
            if curr[i][j] == 0:
                null_it = (i,j)
                break


    final_state = None


    i , j = null_it

    if i+1<3 :

        state = curr.copy()


        k = state[i][j]
        z = state[i+1][j]

        state[i][j] = z
        state[i + 1][j] = k

        tmp = cal_h(state)
        print(tmp)

        if tmp < new_h:
            new_h = tmp
            final_state = state


    if j+1<3 :

        state = curr.copy()

        print(state is curr)
        k = state[i][j]
        z = state[i][j+1]

        state[i][j] = z
        state[i][j + 1] = k

        tmp = cal_h(state)
        print(tmp)

        if tmp < new_h:
            new_h = tmp
            final_state = state


    if i-1>=0 :

        state = curr.copy()


        k = state[i][j]
        z = state[i-1][j]

        state[i][j] = z
        state[i - 1][j] = k

        tmp = cal_h(state)
        print(tmp)

        if tmp < new_h:
            new_h = tmp
            final_state = state


    if j-1>=0 :

        state = curr.copy()


        k = state[i][j]
        z = state[i][j-1]

        state[i][j] = z
        state[i][j - 1] = k

        tmp = cal_h(state)
        print(tmp)

        if tmp < new_h:
            new_h = tmp
            final_state = state


    if final_state==None:
        return False
    else:
        return final_state


def run():

    global curr, h

    h = cal_h(start)
    curr = start.copy()

    while True:

        result = find_best_adj()

        if result == False:
            print(curr,h)
            return curr

        else:
            curr = result.copy()
            h = cal_h(curr)

            if h == 0:
                return curr


if __name__ == '__main__':
    run()

