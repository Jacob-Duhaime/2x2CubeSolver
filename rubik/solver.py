# Jacob Duhaime, CSC 440 Assignment 3

from typing import List
from typing import Optional

import rubik


def shortest_path(
    start: rubik.Position,
    end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:
    # Handling for when two sides meet immediately
    if start == end:
        return []
    
    # Dictionaries starting and ending Point are used
    # to help layout the search direction and to document
    # startIterator and backwardIterator are used to traverse
    # through starting point and ending point
    startingPoint = {start: None}
    endingPoint = {end: None}
    startIterator = {}
    backwardIterator = {}

    # This "for" loop iterates over the rubix cube twists
    # adds i to the startingPoint dict and endingPoint 
    # as iterating values to traverse through them
    for i in rubik.quarter_twists:
        startIterator[i] = i
        backwardIterator[rubik.perm_inverse(i)] = i

    # forward and backward tuple have the startingPoint and
    # endingPoint directory respectively, with them both
    # adding their path to BFS_search
    forwardTuple = (startIterator, startingPoint, endingPoint)
    backwardTuple = (backwardIterator, endingPoint, startingPoint)
    BFS_search = [(start, forwardTuple), (end, backwardTuple), None]
    
    # INVARIANT: THERE  IS AT MOST 7 NODES IN A 2-WAY BFS
    # ANY 2X2 RUBIX CUBE CAN BE SOLVED WITH AT MOST 14 MOVES
    # OUR BFS WILL NEVER HAVE MORE THAN 7 NODES ON EITHER SIDE
    for i in range(7):
        # new BFS search path made to account for
        
        new_BFS_search = []

		# INVARIANT: BFS_search AND new_BFS_search WILL ONLY CONTAIN
        # POSITIONS THAT HAVEN'T BEEN VISITED YET IN THE CURRENT LAYER
        # THERE WILL NEVER BE A DUPLICATE POSITION
        
		# INVARIANT: THE POSITION ADDED TO BFS_search IN THE CURRENT LAYER
        # MUST BE A GREATER NUMBER OF MOVES AWAY FROM ANY OF THE POSITIONS
        # IN THE PRECEEDING LAYERS. THE POSITIONS ARE SEARCHED LEVEL BY LEVEL
        while BFS_search:
            cubePosition = BFS_search.pop(0)

            if cubePosition is None:
                new_BFS_search.append(None)
                continue
            
            currentPosition = cubePosition[0]
            rubixMoves, rubixsPositions, rubixsPositionsSearch = cubePosition[1]

            # While within the rubixMoves list
            # see if the next position is within the
            # rubix cube's positions
            for i in rubixMoves:
                nextPosition = rubik.perm_apply(i, currentPosition)
                if nextPosition in rubixsPositions:
                    continue
                
                # If the nextPosition is not within the rubixPositions
                # then add it to new_BFS_search
                rubixsPositions[nextPosition] = (rubixMoves[i], currentPosition)
                new_BFS_search.append((nextPosition, cubePosition[1]))
				
                if nextPosition in rubixsPositionsSearch:
                    forwardPath = []
                    positionOne = nextPosition
                    
                    # While position one is not empty
                    # equate the ith_position to be the starting
                    # point as position one
                    while positionOne is not None:
                        ith_position = startingPoint[positionOne]

                        if ith_position is None:
                            forwardPath.reverse()
                            break

                        forwardPath.append(ith_position[0])
                        positionOne = ith_position[1]

                    backwardPath = []
                    positionTwo = nextPosition
                    
                    # While position two is not empty:
                    # equate the ith_position to be the starting point
					# as position two
                    while positionTwo is not None:
                        ith_position = endingPoint[positionTwo]

                        if ith_position is None:
                            backwardPath.reverse()
                            break

                        backwardPath.append(ith_position[0])
                        positionTwo = ith_position[1]

                    # Concatenates forward and backwards path with
                    # slice notation to reverse the list  in the next 
					# iteration helping find the shortest path
                    
					# INVARIANT: THE SEARCH WILL TERMINATE WHEN A CONNECTION
                    # BETWEEN THE FORWARD AND BACK SEARCHES ARE FOUND.
                    # THE SHORTEST PATH WILL BE THE CONCATENATION OF THE FORWARD
                    # AND BACK PATHS
                    return forwardPath + backwardPath[::-1]
                
        # Set BFS_search equal to new_BFS_search
        BFS_search = new_BFS_search
        
    return None