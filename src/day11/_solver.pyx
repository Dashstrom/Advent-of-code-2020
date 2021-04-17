import timeit
import time
from copy import deepcopy

DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1),
              (0, 1), (1, 0), (-1, 0), (0, -1))

cpdef parse(str raw):
    cdef long y, dy, x, dx
    seats = [[0 if s == "L" else 1 if s == "#" else -1
              for s in line.strip()] for line in raw.strip().split("\n")]
    nears = [[[(y + dy, x + dx)
               if 0 <= y + dy < len(seats) and 0 <= x + dx < len(line)
               else (-1, -1) for dy, dx in DIRECTIONS]
              for x in range(len(line))]
             for y, line in enumerate(seats)]
    return {"state": seats, "nears": nears}


cpdef part_one(seats):
    cdef int tour=0, x, y, cy, cx, nb_person, occupied_seat
    old = deepcopy(seats["state"])
    while True:
        actual = []
        tour += 1
        have_change = False
        for y, line in enumerate(old):
            actual.append([])
            for x, occupied_seat in enumerate(line):
                if occupied_seat != -1:
                    nb_person = 0
                    for cy, cx in seats["nears"][y][x]:
                        if cy != -1 and old[cy][cx] == 1:
                            nb_person += 1
                    if occupied_seat == 1 and nb_person>=4:
                        have_change = True
                        actual[y].append(0)
                    elif occupied_seat == 0 and nb_person == 0:
                        actual[y].append(1)
                        have_change = True
                    else:
                        actual[y].append(occupied_seat)
                else:
                    actual[y].append(-1)
        tour += 1
        if not have_change:
            return sum_occupied_seats(actual)
        old = actual


cpdef part_two(seats):
    cdef int x, y, cy, cx, dx, dy, nb_person, occupied_seat, i, tour = 0
    old = deepcopy(seats["state"])
    while True:
        actual = []
        tour += 1
        have_change = False
        for y, line in enumerate(old):
            actual.append([])
            for x, occupied_seat in enumerate(line):
                if occupied_seat != -1:
                    nb_person = 0
                    for i, (dy, dx) in enumerate(seats["nears"][y][x]):
                        cy, cx = dy, dx
                        while cy != -1 and old[cy][cx] != 0:
                            if old[cy][cx] == 1:
                                nb_person += 1
                                break
                            cy, cx = seats["nears"][cy][cx][i]
                    if occupied_seat == 1 and nb_person>=5:
                        have_change = True
                        actual[y].append(0)
                    elif occupied_seat == 0 and nb_person == 0:
                        actual[y].append(1)
                        have_change = True
                    else:
                        actual[y].append(occupied_seat)
                else:
                    actual[y].append(-1)
        if not have_change:
            return sum_occupied_seats(actual)
        old = actual

    
cpdef sum_occupied_seats(seats):
    return sum([sum([s for s in line if s == 1]) for line in seats]) 