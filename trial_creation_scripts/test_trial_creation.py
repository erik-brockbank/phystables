from phystables.trials import RedGreenTrial
from phystables.constants import GREENGOAL, GREEN, REDGOAL, RED

TRIAL_DIMS = [800, 800]

def make_test_trial():
    # Name the trial we're making (this will be used when we set up the trial and when we save it)
    name = "test_auto_script"

    # Create a "RedGreenTrial" with the name above and dimensions specified by global TRIAL_DIMS variable
    test_trial = RedGreenTrial(name = name, dims = TRIAL_DIMS)

    # Add walls to our trial
    test_trial.add_wall(upperleft = [50, 50], lowerright = [60, 100])

    # Add a ball to our trial
    test_trial.add_ball(initpos = [300, 300], initvel = [1,1])

    # Add red and green goals to our trial (we always need one of each!)
    test_trial.add_goal(upperleft = [400, 400], lowerright = [410, 500], color = GREEN, onreturn = GREENGOAL)
    test_trial.add_goal(upperleft = [200, 200], lowerright = [250, 210], color = RED, onreturn = REDGOAL)

    # Save our trial to a file so we can run it later
    test_trial.save(flnm = name+".ptr", fldir = "saved_trials")


def main():
    # Make the trial specified in the make_test_trial function above
    make_test_trial()



if __name__ == "__main__":
    main()