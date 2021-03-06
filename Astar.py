import sys

import cv2 as cv
import json
import numpy as np
import base64
from PIL import ImageFile
from flask import make_response


def read_img(file_path):
    temp = []  #
    blueprint = []  # 0 is path, 1is block
    base64_data = open(file_path, 'r').read()
    b = base64.b64decode(base64_data)
    nparr = np.fromstring(b, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    Img = img.tolist()
    X, Y = len(Img[1]), len(Img)
    for y in range(Y):
        for x in range(X):
            if Img[y][x] == [255, 255, 255]:
                temp.append(0)
            else:
                temp.append(1)
        blueprint.append(temp)
    temp = []
    return blueprint


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def heuristic(node, goal):
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return dx + dy


def UseRomListist(Ustr):
    User_List = []
    Ustr = Ustr.replace('[', '')
    Ustr = Ustr.replace(']', '')
    Ustr = Ustr.split(',')
    for i in Ustr:
        User_List.append(tuple(map(int, i.split(':'))))
    return User_List


def RoomList(Rstr):
    Room_List = []
    Rstr = Rstr.replace('[', '')
    Rstr = Rstr.replace(']', '')
    Rstr = Rstr.split(',')
    for i in Rstr:
        Room_List.append(tuple(map(int, i.split(':'))))
    return Room_List


def Astar(maze, start, end):
    # Create start and end node
    startNode = Node(None, start)
    endNode = Node(None, end)
    # Initialize both open and closed list
    openList = []
    closedList = []
    # Add the start node
    openList.append(startNode)
    # Loop until you find the end
    while openList:
        # Get the current node
        currentNode = openList[0]
        currentIdx = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIdx = index
        # Pop current off open list, add to closed list
        openList.pop(currentIdx)
        closedList.append(currentNode)
        # Found the goal
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # reverse
        # Generate children
        children = []
        # ????????? xy?????? ??????
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            # Get node position

            nodePosition = (
                currentNode.position[0] + newPosition[0],  # X
                currentNode.position[1] + newPosition[1])  # Y
            within_range_criteria = [
                nodePosition[0] > (len(maze) - 1),
                nodePosition[0] < 0,
                nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
                nodePosition[1] < 0,
            ]
            if any(within_range_criteria):  # ???????????? true??? ?????? ??????
                continue
            # ???????????? ????????? ?????? ?????? ????????????
            if maze[nodePosition[0]][nodePosition[1]] != 0:
                continue
            new_node = Node(currentNode, nodePosition)
            children.append(new_node)
        # loop all children
        for child in children:
            if child in closedList:
                continue
            # update value f, g, h
            child.g = currentNode.g + 1
            child.h = heuristic(child, endNode)
            child.f = child.g + child.h
            if len([openNode for openNode in openList
                    if child == openNode and child.g > openNode.g]) > 0:
                continue
            openList.append(child)


def Compare(UL, RL):
    RomList = RoomList(RL)
    end = RomList[0][0], RomList[0][1]
    userX, userY = UseRomListist(UL)[0]
    temp = abs(userX - RomList[0][0]) + abs(userY - RomList[0][1])
    for i in range(1, len(RomList)):
        if temp > abs(userX - RomList[i][0]) + abs(userY - RomList[i][1]):
            end = RomList[i][1], RomList[i][0]
    return end


def startAstar(UL, RL, file_path):
    ax = []
    ay = []
    data = []
    rpath = []
    maze = read_img(file_path)
    start = UseRomListist(UL)[0][1], UseRomListist(UL)[0][0]
    # start = y,x
    end = Compare(UL, RL)
    # end = y,x
    path = Astar(maze, start, end)
    for i in path:
        rpath.append(tuple(4 * elem for elem in i))
    for i in rpath:
        ax.append(i[1])
        ay.append(i[0])
    for i in range(len(ax)):
        data.append({'x': ax[i], 'y': ay[i]})
    return (json.dumps(data, ensure_ascii=False, indent='\t'))


def Astar_main(ul, rl, path):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    #UL = argv[0]
    #RL = argv[1]
    #file_path = argv[2]
    #UL = "[154:230]"
    #RL ="[110:36]"
    #file_path = "C:/Users/namu/Desktop/test/74278BDA-B644-4520-8F0C-720EAF059935_1.txt"
    return (startAstar(ul, rl, path))
