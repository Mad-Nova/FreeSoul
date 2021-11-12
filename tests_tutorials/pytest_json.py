import json
import os

"""
class jsonTest():

    def __init__(self):
"""
def testtext():
    print(os.path.abspath('testtext.txt'))
    print("\n")

    f = open('tests_tutorials/testtext.txt')
    print(f.read())
    f.close()


def testjson():
    f = open('tests_tutorials/records.json')
    contents = json.load(f)
    f.close()
    print("Starting file:" + str(contents))

    contents['best_time'] = 5.0
    print("Edited python dictionary:" + str(contents))
    with open('tests_tutorials/records.json', "w") as f:
        json.dump(contents, f)

    f = open('tests_tutorials/records.json')
    contents = json.load(f)
    f.close()
    print("Saved & reopened json file:" + str(contents))


def main():
    print("Output begins\n\n")

    testjson()

    print("\n\nReached end of program")

if __name__ == "__main__":
    main()