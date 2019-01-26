import csv
import os

from phystables.constants import get_const
from phystables.models.point_simulation import PointSimulation
from phystables.trials import load_trial, RedGreenTrial


TRIAL_PATH = "saved_trials"
TRIAL_NAME = "contain_sc1_var_l1_complex_l1" # TODO take this as input arg

OUTPUT_FILE = "containment_sims.csv" # name of csv file to write to
CSV_HEADER = ["trialname", "outcome", "endpoint_x", "endpoint_y", "bounces", "tsims"]

DEFAULTVEL = [175, 180]


def write_to_csv(simname, sim_outcomes, csvwriter):
    for i in range(len(sim_outcomes["outcomes"])):
        # get data
        writedata = [
            simname,
            get_const(sim_outcomes["outcomes"][i]),
            sim_outcomes["endpoints"][i][0],
            sim_outcomes["endpoints"][i][1],
            sim_outcomes["bounces"][i],
            sim_outcomes["tsims"][i]
        ]
        # write data to csv
        csvwriter.writerow(writedata)


def get_ball_vel(currvel):
    newvel = DEFAULTVEL
    # NB: this logic largely copied from similar default handling in phystables_env: objects.js
    if abs(currvel[0]) == 1 or abs(currvel[1]) == 1:
        # Ball has default velocities from trial creation process (e.g. [1, -1])
        newvel = [DEFAULTVEL[0] * currvel[0], DEFAULTVEL[1] * currvel[1]]
    elif abs(currvel[0]) >= 10 or abs(currvel[1]) >= 10:
        # Ball has velocities overriding default from trial creation process
        newvel = currvel

    return newvel


def get_simulation_outcomes(filepath):
    rgtrial = load_trial(filepath)
    # correct ball velocity
    # TODO handle velocity exceptions in particular scenarios
    rgtrial.ball = (rgtrial.ball[0],) + (get_ball_vel(rgtrial.ball[1]),) + (rgtrial.ball[2:len(rgtrial.ball)])
    # make table and simulation object
    rgtable = rgtrial.make_table()
    ps = PointSimulation(rgtable, cpus = 1) # NB: without cpu arg, async_map call in point_simulation fails
    sim = ps.run_simulation()

    assert(len(sim[0]) == len(sim[1]) == len(sim[2]) == len(sim[3]))
    return {"outcomes": sim[0],
            "endpoints": sim[1],
            "bounces": sim[2],
            "tsims": sim[3]}


def main():
    # initialize csv writer
    csv_output = open(OUTPUT_FILE, "w")
    csvwriter = csv.writer(csv_output)
    # write header
    csvwriter.writerow(CSV_HEADER)

    # TODO consider making this a little less ad hoc...
    files = [f for f in os.listdir(TRIAL_PATH) if f.endswith(".json") and
        "contain" in f and
        "distractor" not in f and
        ("sc1" in f or "sc2" in f or "sc3" in f or "sc4" in f)]
    print("Reading in files at {}. Num files: {}".format(TRIAL_PATH, len(files)))

    # simulate trials and write results
    for f in files:
        trialname = f.split('.')[0]
        read_file = os.path.join(TRIAL_PATH, f)
        print("Running simulations for {}".format(read_file))
        sim_outcomes = get_simulation_outcomes(read_file)

        print("Writing {} to csv at: {}".format(trialname, OUTPUT_FILE))
        write_to_csv(trialname, sim_outcomes, csvwriter)

    csv_output.close()



### Simple stub to run the PointSimulator for generating noisy simulations of phystables trials ###
if __name__ == "__main__":
    main()
