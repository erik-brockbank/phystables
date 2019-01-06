import copy
import json
import os
from phystables.trials import load_trial, RedGreenTrial


TRIAL_PATH = "saved_trials"

def print_json(file_json):
    print("name: {} \ndims: {}\nball: {}\ngoals: {}\nwalls: {}\n".format(
        file_json.name,
        file_json.dims,
        file_json.ball,
        file_json.goals,
        file_json.normwalls
    ))

def get_filenames(filepath):
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(filepath):
        for file in filenames:
            # TODO this is a hacky way to deal with these exclusions...
            if "json" in file and \
                file not in file_list and \
                "TEMPLATE" not in file and \
                "LEFT" not in file and \
                "RIGHT" not in file and \
                "TWICE" not in file:
                file_list.append(file)
    file_list = sorted(file_list)
    return file_list

def read_file(filename, filepath):
    read_file = os.path.join(filepath, filename)
    file_json = load_trial(read_file)
    return file_json

def write_file(filepath, filejson):
    filename = filejson.name + ".json"
    write_file = os.path.join(filepath, filename)
    print("Writing data to: {}".format(write_file))

    trial = RedGreenTrial(name = filejson.name, dims = filejson.dims)
    trial.add_ball(initpos = filejson.ball[0],
                    initvel = filejson.ball[1],
                    rad = filejson.ball[2],
                    color = filejson.ball[3],
                    elast = filejson.ball[4])
    for goal in filejson.goals:
        trial.add_goal(upperleft = goal[0],
                        lowerright = goal[1],
                        onreturn = goal[2],
                        color = goal[3])
    for wall in filejson.normwalls:
        trial.add_wall(upperleft = wall[0],
                        lowerright = wall[1],
                        color = wall[2],
                        elast = wall[3])

    trial.save(flnm = filejson.name + ".ptr", fldir = filepath) # save .ptr for viewing with simulator
    trial.save(flnm = filejson.name + ".json", fldir = filepath) # save .json for use in actual experiments

def rotate_coord_right(coord, max_x, max_y):
    new_x = max_x - coord[1]
    new_y = coord[0]
    return (new_x, new_y)

def rotate_coord_left(coord, max_x, max_y):
    new_x = coord[1]
    new_y = max_x - coord[0]
    return (new_x, new_y)

def rotate_coord_twice(coord, max_x, max_y):
    new_x = max_x - coord[0]
    new_y = max_y - coord[1]
    return (new_x, new_y)

def rotate_walls_left(walls_list, dims):
    # works for targets as well since both walls and targets are defined by
    # upper left and lower right coordinates
    for index in range(len(walls_list)):
        wall = walls_list[index]
        top_left_coords, bottom_right_coords = wall[0], wall[1]
        top_left_coords_rotated = rotate_coord_left(top_left_coords, dims[0], dims[1])
        bottom_right_coords_rotated = rotate_coord_left(bottom_right_coords, dims[0], dims[1])
        new_top_left = [top_left_coords_rotated[0], bottom_right_coords_rotated[1]]
        new_bottom_right = [bottom_right_coords_rotated[0], top_left_coords_rotated[1]]
        walls_list[index] = (new_top_left, new_bottom_right) + walls_list[index][2:]
    return walls_list

def rotate_walls_right(walls_list, dims):
    # works for targets as well since both walls and targets are defined by
    # upper left and lower right coordinates
    for index in range(len(walls_list)):
        wall = walls_list[index]
        top_left_coords, bottom_right_coords = wall[0], wall[1]
        top_left_coords_rotated = rotate_coord_right(top_left_coords, dims[0], dims[1])
        bottom_right_coords_rotated = rotate_coord_right(bottom_right_coords, dims[0], dims[1])
        new_top_left = [bottom_right_coords_rotated[0], top_left_coords_rotated[1]]
        new_bottom_right = [top_left_coords_rotated[0], bottom_right_coords_rotated[1]]
        walls_list[index] = (new_top_left, new_bottom_right) + walls_list[index][2:]
    return walls_list

def rotate_walls_twice(walls_list, dims):
    # works for targets as well since both walls and targets are defined by
    # upper left and lower right coordinates
    for index in range(len(walls_list)):
        wall = walls_list[index]
        top_left_coords, bottom_right_coords = wall[0], wall[1]
        top_left_coords_rotated = rotate_coord_twice(top_left_coords, dims[0], dims[1])
        bottom_right_coords_rotated = rotate_coord_twice(bottom_right_coords, dims[0], dims[1])
        new_top_left = [bottom_right_coords_rotated[0], bottom_right_coords_rotated[1]]
        new_bottom_right = [top_left_coords_rotated[0], top_left_coords_rotated[1]]
        walls_list[index] = (new_top_left, new_bottom_right) + walls_list[index][2:]
    return walls_list

def rotate_ball_left(ball, dims):
    # rotate ball coordinates
    ball_coords = ball[0]
    ball_coords_rotated = rotate_coord_left(ball_coords, dims[0], dims[1])
    new_coords = [ball_coords_rotated[0], ball_coords_rotated[1]]
    # rotate ball velocity
    ball_vel = ball[1]
    ball_vel = [ball_vel[0], -1 * ball_vel[1]]

    ball = (new_coords, ball_vel) + ball[2:]
    return ball

def rotate_ball_right(ball, dims):
    # rotate ball coordinates
    ball_coords = ball[0]
    ball_coords_rotated = rotate_coord_right(ball_coords, dims[0], dims[1])
    new_coords = [ball_coords_rotated[0], ball_coords_rotated[1]]
    # rotate ball velocity
    ball_vel = ball[1]
    ball_vel = [-1 * ball_vel[0], ball_vel[1]]

    ball = (new_coords, ball_vel) + ball[2:]
    return ball

def rotate_ball_twice(ball, dims):
    # rotate ball coordinates
    ball_coords = ball[0]
    ball_coords_rotated = rotate_coord_twice(ball_coords, dims[0], dims[1])
    new_coords = [ball_coords_rotated[0], ball_coords_rotated[1]]

    # rotate ball velocity
    ball_vel = ball[1]
    ball_vel = [-1 * ball_vel[0], -1 * ball_vel[1]]

    ball = (new_coords, ball_vel) + ball[2:]
    return ball

def rotate_trial_left(filejson):
    dims = filejson.dims
    ball = filejson.ball
    goals = filejson.goals
    walls = filejson.normwalls

    walls_rotated = rotate_walls_left(walls, dims)
    filejson.normwalls = walls_rotated

    goals_rotated = rotate_walls_left(goals, dims)
    filejson.goals = goals_rotated

    ball_rotated = rotate_ball_left(ball, dims)
    filejson.ball = ball_rotated

    filejson.name = filejson.name + "_LEFT"
    return filejson

def rotate_trial_right(filejson):
    dims = filejson.dims
    ball = filejson.ball
    goals = filejson.goals
    walls = filejson.normwalls

    walls_rotated = rotate_walls_right(walls, dims)
    filejson.normwalls = walls_rotated

    goals_rotated = rotate_walls_right(goals, dims)
    filejson.goals = goals_rotated

    ball_rotated = rotate_ball_right(ball, dims)
    filejson.ball = ball_rotated

    filejson.name = filejson.name + "_RIGHT"
    return filejson

def rotate_trial_twice(filejson):
    dims = filejson.dims
    ball = filejson.ball
    goals = filejson.goals
    walls = filejson.normwalls

    walls_rotated = rotate_walls_twice(walls, dims)
    filejson.normwalls = walls_rotated

    goals_rotated = rotate_walls_twice(goals, dims)
    filejson.goals = goals_rotated

    ball_rotated = rotate_ball_twice(ball, dims)
    filejson.ball = ball_rotated

    filejson.name = filejson.name + "_TWICE"
    return filejson


def main():
    file_list = get_filenames(TRIAL_PATH)
    for filename in file_list:
        print("Processing file: {}".format(filename))
        file_parsed = read_file(filename, TRIAL_PATH)
        file_rotated_left = rotate_trial_left(copy.deepcopy(file_parsed))
        file_rotated_right = rotate_trial_right(copy.deepcopy(file_parsed))
        file_rotated_twice = rotate_trial_twice(copy.deepcopy(file_parsed))

        # print("Original file:")
        # print_json(file_parsed)
        # print("Rotated file (left):")
        # print_json(file_rotated_left)
        # print("Rotated file (right):")
        # print_json(file_rotated_right)
        # print("Rotated file (twice):")
        # print_json(file_rotated_twice)

        write_file(TRIAL_PATH, file_rotated_left)
        write_file(TRIAL_PATH, file_rotated_right)
        write_file(TRIAL_PATH, file_rotated_twice)



"""
To run this:
1. From ~/web/vullab/phystables: python -m trial_creation_scripts.trial_rotator
"""
if __name__ == "__main__":
    main()