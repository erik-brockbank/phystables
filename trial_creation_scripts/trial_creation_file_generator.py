import subprocess


SCENARIO = "contain"
SCENARIO_VARIANTS = 5 # there are 5 containment scenarios
VARIABLE_LEVELS = 3 # there are 3 containment levels in each scenario
COMPLEXITY_LEVELS = 4 # there are 4 complexity levels for each containment level in each scenario
FILE_TEMPLATE_FORMAT = "{}_sc{}_var_l{}_complex_l{}.py" # the above globals will be piped in to the blanks here
FILE_TEMPLATE_NAME = "trial_creation_template.py" # this is the "source" file we're copying to each new file
FILE_PATH = "trial_creation_scripts/"

def main():
    bash_cmd = "cp {} {}"
    for scene_level in range(1, SCENARIO_VARIANTS + 1):
        for var_level in range(1, VARIABLE_LEVELS + 1):
            for complex_level in range(1, COMPLEXITY_LEVELS + 1):
                source_file = FILE_PATH + FILE_TEMPLATE_NAME
                target_file = FILE_PATH + FILE_TEMPLATE_FORMAT.format(
                    SCENARIO, str(scene_level), str(var_level), str(complex_level)
                )
                bash_cmd_formatted = bash_cmd.format(source_file, target_file).split()
                print("Executing: {}".format(bash_cmd_formatted))
                process = subprocess.Popen(bash_cmd_formatted, stdout = subprocess.PIPE)
                output, error = process.communicate()
    print("Complete.")




if __name__ == "__main__":
    main()