
"""
Trial Info

Theme: containment
Scenario: scenario 1
Variable: containment level 1
Complexity: complexity level 1

Status: Incomplete
Assigned to:
Last updated:

Notes:

"""
from constants import BALL_VELOCITY, SAVED_TRIAL_DIR, TRIAL_DIMS
from phystables.trials import RedGreenTrial
from phystables.constants import GREENGOAL, GREEN, REDGOAL, RED


TRIAL_NAME = "template"


# TODO fill in this function and delete this comment once it's complete
def add_ball(trial):
    """
    This function adds the ball to the proper place for this trial
    """
    ball_x = "" # TODO replace these "" with a number and delete this comment!
    ball_y = "" # TODO replace these "" with a number and delete this comment!
    trial.add_ball(initpos = [ball_x, ball_y], initvel = BALL_VELOCITY)
    return trial


def add_targets(trial):
    """
    This function adds the targets to the proper place for this trial
    """
    return trial


def add_walls(trial):
    """
    This function adds the walls to the proper place for this trial
    """
    return trial


def add_obstacles(trial):
    """
    This function adds additional obstacles (small walls) to the proper place for this trial
    """
    return trial


# Don't worry about filling this in
def main():
    trial = RedGreenTrial(name = TRIAL_NAME, dims = TRIAL_DIMS)

    trial = add_ball(trial) # TODO see if we can avoid assignment over and over here
    trial = add_targets(trial)
    trial = add_walls(trial)
    trial = add_obstacles(trial)

    trial.save(flnm = TRIAL_NAME + ".ptr", fldir = SAVED_TRIAL_DIR)


# Ignore this
if __name__ == "__main__":
    main()