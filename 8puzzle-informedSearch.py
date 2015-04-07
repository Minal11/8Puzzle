"""
Name:Minal Kondawar
Username: mkondawa
Assignment 2: Search-based problem solving:8 puzzle 
"""
import time
import sys

#function to move blank up
def moveUp(rootState,visitedNodes,nodes):
  
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
   
    if index not in [0,1,2]:    
        swapvar=newState[index-3]
        newState[index-3]=newState[index]
        newState[index]=swapvar
    
        for temp in visitedNodes:   #to check if state are present in visited nodes: repeated state detection
            if newState==temp.rootState:
                return None
        for temp in nodes:  #repeated state detection  
            if newState==temp.rootState:
                return None
        
        return newState
    else:
       
        return None
    
#function to move blank down
def moveDown(rootState,visitedNodes,nodes):
   
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
    
    if index not in [6,7,8]:
        swapvar=newState[index+3]
        newState[index+3]=newState[index]
        newState[index]=swapvar
    
        for temp in visitedNodes: #repeated state detection check
            if newState==temp.rootState:
                return None
        for temp in nodes: #repeated state detection  check
            if newState==temp.rootState:
                return None
        #OutputProcedure(newState)
        return newState
    else:
       
        return None

#function to move blank left    
def moveLeft(rootState,visitedNodes,nodes):
  
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
  
    
    if index not in [0,3,6]:
        swapvar=newState[index-1]
        newState[index-1]=newState[index]
        newState[index]=swapvar
     
        for temp in visitedNodes:   #repeated state detection check
            if newState==temp.rootState:
                return None
        for temp in nodes: #repeated state detection check
            if newState==temp.rootState:
                return None
      
        return newState
    else:
       
        return None

#function to move blank right 
def moveRight(rootState, visitedNodes,nodes):
   
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
    if index not in [2,5,8]:
        swapvar=newState[index+1]
        newState[index+1]=newState[index]
        newState[index]=swapvar
     
       
        for temp in visitedNodes: #repeated state detection check 
            if newState==temp.rootState:
                return None
        for temp in nodes:  #repeated state detection check
            if newState==temp.rootState:
                return None
        
        return newState
    else:
        
        return None

#function to calculate heuristic       
def calc_heuristic(func_name,state,goalState):
    if func_name=="a_star" or func_name=="hamming":
        heuristic=h(state,goalState)
    else:
        heuristic=mhd(state,goalState)
    return heuristic

#function to create children
def successor(node, nodes,visitedNodes,func_name,goalState):
  
    children=[]

    state=moveUp(node.rootState,visitedNodes,nodes)
    heuristic=calc_heuristic(func_name,state,goalState)
    children.append(makeNode(state,node,"movedup",node.depth+1,heuristic,func_name))#add the state after moving up
  
    state=moveDown(node.rootState,visitedNodes,nodes)
    heuristic=calc_heuristic(func_name,state,goalState)
    children.append(makeNode(state,node,"movedDown",node.depth+1,heuristic,func_name))#add the state after moving down
    
    state=moveLeft(node.rootState,visitedNodes,nodes)
    heuristic=calc_heuristic(func_name,state,goalState)
    children.append(makeNode(state,node,"movedLeft",node.depth+1,heuristic,func_name))#add the state after moving left
   
    state=moveRight(node.rootState,visitedNodes,nodes)
    heuristic=calc_heuristic(func_name,state,goalState)
    children.append(makeNode(state,node,"movedRight",node.depth+1,heuristic,func_name))#add the state after moving right

    #taking all the none from children using list comprehension
    children=[node for node in children if node.rootState!=None]
    
    return children




class Node:
    def __init__(self,rootState,parentState,movement,depth,h,func_name):
        self.rootState=rootState #stores root state
        self.parentState=parentState #stores parent state
        self.movement=movement #stores movement like "u:up d:dowm l:left r:right"
        self.depth=depth #stores depth of current state
        self.func_name=func_name
        if func_name=="a_star":
            self.h=h+depth  #for a_star f(n)=g(n)+h(n)
        else:
            self.h=h #for best first search f(n)=h(n)
       
    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.depth,
                                  self.h)                            

#function to make node
def makeNode(rootState,parentState,movement,depth,h,func_name):
   
    return Node(rootState,parentState,movement,depth,h,func_name)

#general search
def GeneralSearch(initialState, goalState,limit,func_name ):    
    nodes = []
    visitedNodes=[]
    no=[]
    num=0
    nodes.append( makeNode(initialState, None, None, 0,0,func_name) )
   
    while True:
        if len( nodes ) == 0:
            return None
        if limit==0:
            return 0
        node = nodes.pop(0)
        limit=limit-1
        visitedNodes.append(node)
        #if not equal to goal state, create children of nodes
        if not testProcedure(node,goalState):
            no=successor( node, nodes,visitedNodes,func_name,goalState )
            nodes.extend(no)
            num=num+len(no)#for number of states generated
            nodes=sorted(nodes,key=getKey) #sorting the list to form it priority queue that is-it is list that has node with minimum heuristic at first
        else:
           
            list_of_moves=findPath_and_moves(node,num)
            return list_of_moves
        
def getKey(node):
    
    return node.h
   
#function to create path  and moves
def findPath_and_moves(node, num):
    
    path.insert(0,node.rootState)   #to keep the track of path
    moves=[]
    temp=node
    while True:
        moves.insert(0,temp.movement) #insert at start of list-length of moves will be total moves
        if temp.depth<=1:   #when initial and goal is same 
            break
        temp=temp.parentState
        path.insert(0,temp.rootState)
       
    print "total number of moves:",num
    return moves

#function to test with goal state
def testProcedure(node,goalState):

    if node.rootState==goalState:
            return True
    return False


#calculating the misplace tiles
def h( state, goal ):
    misplace_no = 0
    if state==None:
            return 0
    for i in range(0,9):
        
        if state[i] != goal[i]:
            misplace_no = misplace_no + 1
            #print "score",score
    return misplace_no

#calculating the manhattan distance
def mhd(state,goal):
    
    sum = 0
    
    if state==None:
        return 0
    for c in range(0,9):
        sum =sum + dist(state.index(c), goal.index(c))
    return sum

def dist(n, m):
    x1,y1 = xyLocation[n]
    x2,y2 = xyLocation[m]
    return abs(x1-x2) + abs(y1-y2)

#function to diplay the state
def OutputProcedure( state ):
    for i in range(9):
        val = state[i]
        if val==0:
            print '.',
        else:
            print val,
        if (i+1)%3==0:
            print


def testInformedSearch1(initialState, goalState,limit):
   
    print "--------------Informed Search using Hamming Distance heuristic (Misplace tiles)-------------------"
    s=time.clock()
    finalOutcome=GeneralSearch(initialState,goalState,limit,"hamming")
    e=time.clock();
    print "Time taken to solve:","%.3f" % (e - s),"secs"
    if finalOutcome==None:
        print "No solution found"
    elif finalOutcome==[None]:
        print "Initial state is same as Goal state"
    elif finalOutcome==0:
        print "Reached the limit"
    else:
        print finalOutcome
        print "Total",len(finalOutcome),"moves"
    print "initial state"

    if finalOutcome!=0:
        OutputProcedure(initialState)

        print "Path"
        move_count=len(path)
        j=0
        while(move_count):
            OutputProcedure(path[j])
            j=j+1
            move_count=move_count-1

def testInformedSearch2(initialState, goalState,limit):
    
    print "--------------Informed Search using Manhattan Distance heuristic -------------------"
    s=time.clock()
    finalOutcome=GeneralSearch(initialState,goalState,limit,"manhattan")
    e=time.clock();
    print "Time taken to solve:","%.3f" % (e - s),"secs"
    if finalOutcome==None:
        print "No solution found"
    elif finalOutcome==[None]:
        print "Initial state is same as Goal state"
    elif finalOutcome==0:
        print "Reached the limit"
    else:
        print finalOutcome
        print "Total",len(finalOutcome),"moves"
    print "initial state"

    if finalOutcome!=0:
        OutputProcedure(initialState)

        print "Path"
        move_count=len(path)
        j=0
        while(move_count):
            OutputProcedure(path[j])
            j=j+1
            move_count=move_count-1
   
def testAStar(initialState, goalState, limit):
    print "--------------A * Algorithm using hamming distance heuristic-------------------"
    s=time.clock()
    finalOutcome=GeneralSearch(initialState,goalState,limit,"a_star")
    e=time.clock();
    print "Time taken to solve:","%.3f" % (e - s),"secs"
    if finalOutcome==None:
        print "No solution found"
    elif finalOutcome==[None]:
        print "Initial state is same as Goal state"
    elif finalOutcome==0:
        print "Reached the limit"
    else:
        print finalOutcome
        print "Total",len(finalOutcome),"moves"
    print "initial state"

    if finalOutcome!=0:
        OutputProcedure(initialState)

        print "Path"
        move_count=len(path)
        j=0
        while(move_count):
            OutputProcedure(path[j])
            j=j+1
            move_count=move_count-1

def makeState(nw, n, ne, w, c, e, sw, s, se):
    state=[]
    if nw!="blank":
        state.append(nw)
    else:
        state.append(0)
    if n!="blank":
        state.append(n)
    else:
        state.append(0)
    if ne!="blank":
        state.append(ne)
    else:
        state.append(0)
    if w!="blank":
        state.append(w)
    else:
        state.append(0)
    if c!="blank":
        state.append(c)
    else:
        state.append(0)
    if e!="blank":
        state.append(e)
    else:
        state.append(0)
    if sw!="blank":
        state.append(sw)
    else:
        state.append(0)
    if s!="blank":
        state.append(s)
    else:
        state.append(0)
    if se!="blank":
        state.append(se)
    else:
        state.append(0)
    
    return state 


xyLocation = {0:(0,0), 1:(1,0), 2:(2,0),
               3:(0,1), 4:(1,1), 5:(2,1),
               6:(0,2), 7:(1,2), 8:(2,2)}

#create initial and goal state using makeState  function
init=makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
goal=makeState(1,2,3,4,5,6,7,8,"blank")
print "Goal State"
OutputProcedure(goal)
print "Initial State"
OutputProcedure(init)


print "***************Search Started******************"
path=[]
testInformedSearch1(init, goal, 2000)
path=[]
testInformedSearch2(init, goal, 2000)
path=[]
testAStar(init, goal, 2000)

print "**************Search Completed******************"




