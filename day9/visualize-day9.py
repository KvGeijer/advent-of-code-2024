import heapq

with open('input.txt') as f:
    ints = [int(c) for c in f.read().strip()]

# For each size of vacancy, we have the start_ind here.
# These don't have to be valid, if the space before or after is also empty, it is inconsistent
# This should be consistent at the start of every operation
paddings = [[] for _ in range(10)]

# list of (start_ind, size)
starting_mem_regs = []


def find_best(size, swap_start):
    best_start = swap_start + 1
    best_size = None
    for bucket_size in range(size, 10):
        bucket = paddings[bucket_size]

        # Pop invalid paddings
        while bucket and ((mem[bucket[0]] == -1 and mem[bucket[0] - 1] == -1) or mem[bucket[0]] != -1):
            heapq.heappop(bucket)

        if bucket and bucket[0] <= best_start and bucket[0] < swap_start:
            best_start = bucket[0]
            best_size = bucket_size

    if best_start < swap_start:
        # We pop it from the data structure
        heapq.heappop(paddings[best_size])
        return (best_start, best_size)
    else:
        return None


ind = 0
mem = [0 for i in range(sum(ints) + 9)]
for (i, size) in enumerate(ints):
    if i % 2 == 0:
        # not padding
        starting_mem_regs.append((ind, size))
        id = i//2
        for _ in range(size):
            mem[ind] = id
            ind += 1
    else:
        # padding
        heapq.heappush(paddings[size], ind)
        for _ in range(size):
            mem[ind] = -1
            ind += 1

for (start_ind, size) in starting_mem_regs[::-1]:
    if size == 0:
        continue

    id = mem[start_ind]
    # Try to place it somewhere
    # As we do part 2, we only want to move the whole thing at once
    if res := find_best(size, start_ind):
        (swap_start, swap_size) = res

        # Now we swap in the memory
        # We insert back the new padding
        # However, we must also add padding to where we took it from.

        # Wipe out the memory of the use block
        for ind in range(start_ind, start_ind + size):
            mem[ind] = -1
        # find the new padding
        padding_start = start_ind
        while mem[padding_start - 1] == -1:
            padding_start -= 1

        padding_stop = start_ind
        while mem[padding_stop] == -1:
            padding_stop += 1

        # Push the newly available padding
        padding_size = min(9, padding_stop - padding_start)
        heapq.heappush(paddings[padding_size], padding_start)

        # Now Write the id into the new place
        for ind in range(swap_start, swap_start + size):
            mem[ind] = id

        # WHat is the size of the new padding?
        padding_start = padding_stop = swap_start + size
        while mem[padding_stop] == -1:
            padding_stop += 1

        padding_size = min(9, padding_stop - padding_start)
        heapq.heappush(paddings[padding_size], padding_start)

# Validate result for part 2
tot = 0
for (i, id) in enumerate(mem):
    if id > 0:
        tot += id*i
print(tot)
