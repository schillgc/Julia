def versionCheck(v1, v2):
    char_v1 = v1.split(".")
    char_v2 = v2.split(".")

    # Checks the number of sets of numbers within both version numbers.
    def lengthCheck(char_v1, char_v2):
        len_v1 = len(char_v1)
        len_v2 = len(char_v2)
        if len_v1 >= len_v2:
            toBeCleaned = len_v1 - len_v2
            toBeAddedTo = char_v2
        elif len_v2 >= len_v1:
            toBeCleaned = len_v2 - len_v1
            toBeAddedTo = char_v1
        else:
            print("Not a valid entry")
        return(toBeCleaned, toBeAddedTo)

    try:
        toBeCleaned, toBeAddedTo = lengthCheck(char_v1, char_v2)
        if toBeAddedTo != "":
            for i in range(0, int(toBeCleaned)):
                toBeAddedTo.append("0")

        for i in range(0, len(char_v2), 2):
            if char_v1[i].isdigit() and char_v2[i].isdigit():
                if char_v1[i] > char_v2[i] or not char_v2[i]:
                    results = 1
                    print("v1:", v1, "v2:", v2, "Copy 1 is the higher version")
                    break
                elif char_v1[i] < char_v2[i] or not char_v1[i]:
                    results = -1
                    print("v1:", v1, "v2:", v2, "Copy 2 is the higher version")
                    break
                elif char_v1[i] == char_v2[i]:
                    results = 0
                    if i == 2:
                        print("They are duplicate copies")
                else:
                    print("An error has occurred calculating the results")

            else:
                # For additional questions
                def redo():
                    print("Sorry an error occurred because you entered an invalid key or syntax")
                    v1 = input("Please input your first version number: ")
                    v2 = input("Please input your second version number: ")
                    versionCheck(v1, v2)
                redo()

    except ValueError:
        redo()

versionCheck("1", "1.0.0")
versionCheck("1.0.2", "1.0.1")
versionCheck("1.0.9", "5.0.0")
versionCheck("4.9.0", "49.0")
versionCheck("0.5", "0.500")
versionCheck("", "")
