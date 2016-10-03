from __future__ import print_function

import random
import argparse

from testrail import TestRail

# Dictionary mapping of your project IDs to identifiable names
project_dict = {
    'project1': 1,
    'project2': 2,
}


def get_args():
    project_choices = sorted(project_dict.keys())

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'project', type=str, choices=project_choices,
        help="Project to test")

    return parser.parse_args()


def main():
    """ This will offer a step by step guide to create a new run in TestRail,
        update tests in the run with results, and close the run
    """
    # Parse command line arguments
    args = get_args()

    # Instantiate the TestRail client
    # Use the CLI argument to identify which project to work with
    tr = TestRail(project_dict[args.project])

    # Get a reference to the current project
    project = tr.project(project_dict[args.project])

    # To create a new run in TestRail, first create a new, blank run
    # Update the new run with a name and project reference
    new_run = tr.run()
    new_run.name = "Creating a new Run through the API"
    new_run.project = project
    new_run.include_all = True  # All Cases in the Suite will be added as Tests

    # Add the run in TestRail. This creates the run, and returns a run object
    run = tr.add(new_run)

    print("Created new run: {0}".format(run.name))

    # Before starting the tests, lets pull in the Status objects for later
    PASSED = tr.status('passed')
    FAILED = tr.status('failed')
    BLOCKED = tr.status('blocked')

    # Get a list of tests associated with the new run
    tests = list(tr.tests(run))

    print("Found {0} tests".format(len(tests)))

    # Execute the tests, marking as passed, failed, or blocked
    for test_num, test in enumerate(tests):
        print("Executing test #{0}".format(test_num))
        # Run your tests here, reaching some sort of pass/fail criteria
        # This example will pick results at random and update the tests as such

        test_status = random.choice([PASSED, FAILED, BLOCKED])

        print("Updating test  #{0} with a status of {1}".format(test_num,
                                                               test_status.name))

        # Create a blank result, and associate it with a test and a status
        result = tr.result()
        result.test = test
        result.status = test_status
        result.comment = "The test case was udpated via a script"

        # Add the result to TestRail
        tr.add(result)

    # All tests have been executed. Close this test run
    print("Finished, closing the run")
    tr.close(run)


if __name__ == "__main__":
    main()
