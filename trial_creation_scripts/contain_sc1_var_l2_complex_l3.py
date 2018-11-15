
"""
Trial Info

Theme: containment
Scenario: scenario 1
Variable: containment level 2
Complexity: complexity level 3

Status: Incomplete
Assigned to:
Last updated:

Notes:

"""
import random
from constants import BALL_VELOCITY, SAVED_TRIAL_DIR, TRIAL_DIMS
from phystables.trials import RedGreenTrial
from phystables.constants import GREENGOAL, GREEN, REDGOAL, RED


TRIAL_NAME = "contain_sc1_var_l2_complex_l3"


# TODO fill in this function and delete this comment once it's complete
def add_ball(trial):
    """
    This function adds the ball to the proper place for this trial.
    How to fill this out:
    1. Add the proper X,Y coordinate values for the ball by replacing each ""
        with a number indicating the X or Y value
    """
    ball_x = "" # TODO replace these "" with a number and delete this comment!
    ball_y = "" # TODO replace these "" with a number and delete this comment!
    trial.add_ball(initpos = [ball_x, ball_y], initvel = BALL_VELOCITY)


# TODO fill in this function and delete this comment once it's complete
def add_targets(trial):
    """
    This function adds the targets to the proper place for this trial.
    Note target 1 and target 2 can refer to either the red or the green target:
    we'll randomly assign at the end.
    How to fill this out:
    1. Add the proper X,Y coordinate values for target 1 and target 2 by replacing each ""
        with a number indicating the upper left or bottom right X or Y value
    """
    # target 1 X,Y coordinates assigned to upper left and lower right corners of the target
    target_1_upper_left_x = "" # TODO replace these "" with a number and delete this comment!
    target_1_upper_left_y = "" # TODO replace these "" with a number and delete this comment!
    target_1_lower_right_x = "" # TODO replace these "" with a number and delete this comment!
    target_1_lower_right_y = "" # TODO replace these "" with a number and delete this comment!
    target_1_upper_left_coords = [target_1_upper_left_x, target_1_upper_left_y]
    target_1_lower_right_coords = [target_1_lower_right_x, target_1_lower_right_y]

    # target 2 X,Y coordinates assigned to upper left and lower right corners of the target
    target_2_upper_left_x = "" # TODO replace these "" with a number and delete this comment!
    target_2_upper_left_y = "" # TODO replace these "" with a number and delete this comment!
    target_2_lower_right_x = "" # TODO replace these "" with a number and delete this comment!
    target_2_lower_right_y = "" # TODO replace these "" with a number and delete this comment!
    target_2_upper_left_coords = [target_2_upper_left_x, target_2_upper_left_y]
    target_2_lower_right_coords = [target_2_lower_right_x, target_2_lower_right_y]

    # Randomly assign target 1, target 2 to red and green
    if random.randint(0, 1) == 1:
        target_1_color = GREEN
        target_1_goal = GREENGOAL
        target_2_color = RED
        target_2_goal = REDGOAL
    else:
        target_1_color = RED
        target_1_goal = REDGOAL
        target_2_color = GREEN
        target_2_goal = GREENGOAL

    # Add target 1, target 2 to trial
    trial.add_goal(
        upperleft = target_1_upper_left_coords,
        lowerright = target_1_lower_right_coords,
        color = target_1_color,
        onreturn = target_1_goal
    )
    trial.add_goal(
        upperleft = target_2_upper_left_coords,
        lowerright = target_2_lower_right_coords,
        color = target_2_color,
        onreturn = target_2_goal
    )


# TODO fill in this function and delete this comment once it's complete
def add_walls(trial):
    """
    This function adds the walls to the proper place for this trial.
    How to fill this out:
    1. Add the first wall by simply replacing each of the empty strings below ("") with X,Y coords for a wall
    2. Add subsequent walls by copying the wall you filled in (including the `{` and `}`), then
        pasting it immediately below your existing wall(s) and putting the proper X,Y coords for the new wall
    """
    # TODO fill this in by adding walls to the list and filling out their coordinates
    walls_list = [
        # Individual wall definition starts below this line
        {
            "upper_left_x": "", # TODO replace these "" with a number and delete this comment!
            "upper_left_y": "", # TODO replace these "" with a number and delete this comment!
            "lower_right_x": "", # TODO replace these "" with a number and delete this comment!
            "lower_right_y": "", # TODO replace these "" with a number and delete this comment!
        },
        # Individual wall definition ends above this line
    ]

    # Add each wall in the `walls_list` above to the trial
    for wall in walls_list:
        trial.add_wall(
            upperleft = [wall["upper_left_x"], wall["upper_left_y"]],
            lowerright = [wall["lower_right_x"], wall["lower_right_y"]]
        )


# Ignore this function for now, we'll decide later whether to fill it in manually
def add_obstacles(trial):
    """
    This function adds additional obstacles (small walls) to the proper place for this trial.
    """
    return


# Don't worry about filling this in
def main():
    trial = RedGreenTrial(name = TRIAL_NAME, dims = TRIAL_DIMS)
    add_ball(trial)
    add_targets(trial)
    add_walls(trial)
    add_obstacles(trial)
    trial.save(flnm = TRIAL_NAME + ".ptr", fldir = SAVED_TRIAL_DIR) # save .ptr for viewing with simulator
    trial.save(flnm = TRIAL_NAME + ".json", fldir = SAVED_TRIAL_DIR) # save .json for use in actual experiments

# Ignore this
if __name__ == "__main__":
    main()