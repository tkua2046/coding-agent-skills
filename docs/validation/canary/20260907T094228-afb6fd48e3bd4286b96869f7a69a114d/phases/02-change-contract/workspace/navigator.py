DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def _next_pose(pose):
    x, y, heading = pose
    dx, dy = DIRECTIONS[heading]
    return x + dx, y + dy, heading


def run(pose, commands, occupied=()):
    occupied = set(occupied)
    outcomes = []
    for command in commands:
        x, y, heading = pose
        if command == "F":
            candidate = _next_pose(pose)
            if candidate[:2] in occupied:
                outcomes.append(False)
                continue
            pose = candidate
        elif command == "R":
            pose = (x, y, (heading + 1) % 4)
        elif command == "L":
            pose = (x, y, (heading - 1) % 4)
        else:
            raise ValueError("unknown command")
        outcomes.append(True)
    return pose, outcomes
