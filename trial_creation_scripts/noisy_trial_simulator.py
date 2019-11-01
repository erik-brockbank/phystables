"""
Script for running simulation analysis for phystables environments
To run this:
- cd phystables (root of repo)
- python -m trial_creation_scripts.noisy_trial_simulator
Output writes to csv file in root
"""
import csv
import os

from phystables.constants import get_const
from phystables.models.point_simulation import PointSimulation
from phystables.trials import load_trial, RedGreenTrial
from phystables.visualize import vizmodels


TRIAL_PATH = "saved_trials"

OUTPUT_FILE = "analysis/containment_sims.csv"

CSV_HEADER = ["trialname", "simulation_number", "max_simulation_time", # simulation variables
                "outcome", "endpoint_x", "endpoint_y", "bounces", "simulation_time"] # values

MAX_SIMTIME = 60
SIMULATIONS = 200 # 200 is the default in PointSimulation

DEFAULTVEL = [175, 180]

MODIFIED_TRIALS = {
    "contain_sc1_var_l1_complex_l2_LEFT": [175, -175],
    "contain_sc1_var_l1_complex_l2_RIGHT": [-175, 175],
    "contain_sc1_var_l1_complex_l3": [175, 180],
    "contain_sc1_var_l1_complex_l3_LEFT": [175, -175],
    "contain_sc1_var_l1_complex_l3_RIGHT": [-175, 175],
    "contain_sc1_var_l1_complex_l4_LEFT": [175, -175],
    "contain_sc1_var_l1_complex_l4_RIGHT": [-175, 175],
    "contain_sc1_var_l2_complex_l4_LEFT": [175, -175],
    "contain_sc1_var_l2_complex_l4_RIGHT": [-175, 175],
    "contain_sc2_var_l1_complex_l3": [175, 180],
    "contain_sc2_var_l1_complex_l3_LEFT": [175, -170],
    "contain_sc2_var_l1_complex_l3_RIGHT": [-175, 170],
    "contain_sc3_var_l3_complex_l4_LEFT": [175, -175],
    "contain_sc3_var_l3_complex_l4_RIGHT": [-175, 175],
    "contain_sc4_var_l1_complex_l2": [175, 175],
    "contain_sc4_var_l1_complex_l2_LEFT": [175, -175],
    "contain_sc4_var_l1_complex_l2_RIGHT": [-175, 175],
    "contain_sc4_var_l1_complex_l2_TWICE": [-175, -175],
    "contain_sc4_var_l2_complex_l2": [175, 175],
    "contain_sc4_var_l2_complex_l2_LEFT": [175, -175],
    "contain_sc4_var_l2_complex_l2_RIGHT": [-175, 175],
    "contain_sc4_var_l2_complex_l2_TWICE": [-175, -175]
}


def get_scenario_files(filepath):
    # TODO consider making this a little less ad hoc...
    files = [f for f in os.listdir(filepath) if f.endswith(".json") and
        "contain" in f and
        "distractor" not in f and
        ("sc1" in f or "sc2" in f or "sc3" in f or "sc4" in f)]
    files = sorted(files)

    return files



def write_to_csv(simname, simtime, sim_outcomes, csvwriter):
    for i in range(len(sim_outcomes["outcomes"])):
        # get data
        writedata = [
            simname,
            i + 1,
            simtime,
            get_const(sim_outcomes["outcomes"][i]),
            sim_outcomes["endpoints"][i][0],
            sim_outcomes["endpoints"][i][1],
            sim_outcomes["bounces"][i],
            sim_outcomes["simulation_time"][i]
        ]
        # write data to csv
        csvwriter.writerow(writedata)


def get_ball_vel(trialname, currvel):
    newvel = DEFAULTVEL
    # NB: this logic largely copied from similar default handling in phystables_env: objects.js
    if trialname in MODIFIED_TRIALS:
        # Ball has velocities overriding default from trial creation process
        newvel = MODIFIED_TRIALS[trialname]
    elif abs(currvel[0]) == 1 or abs(currvel[1]) == 1:
        # Ball has default velocities from trial creation process (e.g. [1, -1])
        newvel = [DEFAULTVEL[0] * currvel[0], DEFAULTVEL[1] * currvel[1]]

    return newvel


def get_simulation_outcomes(trialname, filepath, simtime, nsims):
    rgtrial = load_trial(filepath)
    # correct ball velocity
    new_vel = get_ball_vel(trialname, rgtrial.ball[1])
    rgtrial.ball = (rgtrial.ball[0],) + (new_vel,) + (rgtrial.ball[2:len(rgtrial.ball)])
    # make table and simulation object
    rgtable = rgtrial.make_table()
    ps = PointSimulation(rgtable, nsims = nsims, maxtime = simtime, cpus = 1) # NB: without cpu arg, async_map call in point_simulation fails
    sim = ps.run_simulation()

    # this probably draws the trials (?) but doesn't seem to work quite right
    # vizmodels.psdraw_density(ps)

    assert(len(sim[0]) == len(sim[1]) == len(sim[2]) == len(sim[3]))
    return {"outcomes": sim[0],
            "endpoints": sim[1],
            "bounces": sim[2],
            "simulation_time": sim[3]}


def main():
    # initialize csv file
    csv_output = open(OUTPUT_FILE, "w")
    csvwriter = csv.writer(csv_output)
    csvwriter.writerow(CSV_HEADER)

    # get relevant scenario files for simulation
    scenario_files = get_scenario_files(TRIAL_PATH)
    print("Reading in files. Num files: {}".format(len(scenario_files)))

    # simulate trials and write results
    for f in scenario_files:
        trialname = f.split(".")[0]
        read_file = os.path.join(TRIAL_PATH, f)
        print("Running simulations for {}".format(read_file))
        sim_outcomes = get_simulation_outcomes(trialname, read_file, MAX_SIMTIME, SIMULATIONS)

        print("Writing {} to csv at: {}".format(trialname, OUTPUT_FILE))
        write_to_csv(trialname, MAX_SIMTIME, sim_outcomes, csvwriter)

    csv_output.close()
    print("Complete")



if __name__ == "__main__":
    main()
