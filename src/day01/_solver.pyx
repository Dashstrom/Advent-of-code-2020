cpdef int part_one(puzzle):
    cdef int i, j, k, target, length = len(puzzle)
    for i in range(length):
        first = puzzle[i]
        target = 2020 - first
        for j in range(i, length):
            if puzzle[j] == target:
                return puzzle[i] * puzzle[j]


cpdef int part_two(puzzle):
    cdef int i, j, k, first, second, target, lower, length = len(puzzle)
    for i in range(length):
        first = puzzle[i]
        lower = 2020 - first
        for j in range(i, length):
            second = puzzle[j]
            if second <= lower:
                target = lower - second
                for k in range(j, length):
                    if puzzle[k] == target:
                        return first * second * puzzle[k]
        
        

