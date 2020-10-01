import os
from parseFile import parse_file

tests_dir_name = "tests"

All = 0
Passed = 0
Failed = 0
for fn in os.listdir(tests_dir_name):
    All += 1
    print("---Test from '%s'. Parser output:" % fn)
    is_correct = parse_file(tests_dir_name + '/' + fn)
    if is_correct != (fn[0] == 'c'):
        print("---Test from file", fn, "FAILED\n\n")
        Failed += 1
    else:
        print("---Test passed\n\n")
        Passed += 1

print("Number of tests:", All, "      passed: ", Passed, "      failed:", Failed)



