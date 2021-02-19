import json
import copy
import random

filepath = input(
    "What is the name of your students.json file? Or do you need to create one (create)?"
)
if filepath == "create":
    filepath = input("What would you like to call your json file?")
    all_students = []
    while True:
        line = input("What is the students name in the format Last,First ? Or (end).")
        if line == "end":
            break
        student = {
            "name": line,
            "number": 123,  # manually edit for convenience
            "manager": 0,
            "skeptic": 0,
            "experimentalist": 0,
            "archivist": 0,
            "present_days": 0,
            "absent_days": 0,
        }
        all_students.append(student)
        with open(filepath, "w+") as f:
            json.dump({"students": all_students}, f)
with open(filepath, "r+") as f:
    all_students = json.load(f)["students"]
active_students = copy.deepcopy(all_students)
groups = []


def listStudents():
    global all_students
    global active_students
    present_students = []
    absent_students = []

    for student in all_students:
        if student in active_students:
            present_students.append(student)
        else:
            absent_students.append(student)

    print("")
    print("Present Students (%s)" % len(present_students))
    for student in present_students:
        print(student["name"])

    print("")
    print("Absent Students (%s)" % len(absent_students))
    for student in absent_students:
        print(student["name"])


def assignStudentsToGroups():
    global groups
    groups = []
    students = copy.deepcopy(active_students)
    random.shuffle(students)
    num_of_students_unassigned = len(students)
    num_of_3_groups = 2  # always keep at least 2 groups of 3
    num_of_students_unassigned -= num_of_3_groups * 3
    num_of_4_groups = int(num_of_students_unassigned / 4)
    num_of_students_unassigned -= num_of_4_groups * 4
    if num_of_students_unassigned == 3:
        num_of_3_groups += 1
        num_of_students_unassigned = 0
    else:
        while num_of_students_unassigned != 0:
            num_of_4_groups -= 1
            num_of_students_unassigned += 4
            if num_of_students_unassigned % 3 == 0:
                num_of_3_groups += num_of_students_unassigned / 3
                num_of_students_unassigned = 0

    # now we know how many groups to make
    for i in range(0, num_of_4_groups):
        # group of 4 logic
        students_in_group = []
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        group = createGroup(students_in_group)
        groups.append(group)

    for i in range(0, int(num_of_3_groups)):
        # group of 3 logic
        students_in_group = []
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        group = createGroup(students_in_group)
        groups.append(group)
    print("Groups Assigned")


def createGroup(students_in_group):
    manager = {"name": "None", "manager": 100}
    experimentalist = {"name": "None", "experimentalist": 100}
    skeptic = {"name": "None", "skeptic": 100}
    archivist = {"name": "None", "archivist": 100}
    students_left_to_assign = copy.deepcopy(students_in_group)
    for student in students_left_to_assign:
        if student["manager"] < manager["manager"]:
            manager = student
    students_left_to_assign.remove(manager)
    for student in students_left_to_assign:
        if student["experimentalist"] < experimentalist["experimentalist"]:
            experimentalist = student
    students_left_to_assign.remove(experimentalist)
    for student in students_left_to_assign:
        if student["skeptic"] < skeptic["skeptic"]:
            skeptic = student
    students_left_to_assign.remove(skeptic)

    if len(students_in_group) == 4:
        archivist = students_left_to_assign.pop()

    group = {
        "manager": manager,
        "skeptic": skeptic,
        "experimentalist": experimentalist,
        "archivist": archivist,
    }

    return group


def fixGroups():
    global groups
    fixed_groups = copy.deepcopy(groups)
    unassigned_students = []
    for student in active_students:
        present = False
        for group in groups:
            if group["manager"]["name"] == student["name"]:
                present = True
                break
            elif group["skeptic"]["name"] == student["name"]:
                present = True
                break
            elif group["experimentalist"]["name"] == student["name"]:
                present = True
                break
            elif group["archivist"]["name"] == student["name"]:
                present = True
                break
        if not present:
            unassigned_students.append(student)

    groups_of_4 = []
    groups_of_3 = []
    groups_of_2 = []
    groups_of_1 = []
    for group in groups:
        num_of_members = 0
        if group["manager"] in active_students:
            num_of_members += 1
        if group["skeptic"] in active_students:
            num_of_members += 1
        if group["experimentalist"] in active_students:
            num_of_members += 1
        if group["archivist"] in active_students:
            num_of_members += 1
        if num_of_members == 4:
            groups_of_4.append(group)
        if num_of_members == 3:
            groups_of_3.append(group)
        if num_of_members == 2:
            groups_of_2.append(group)
        if num_of_members == 1:
            groups_of_1.append(group)

    # destroy all groups of 1 and add to unassigned
    for group in groups_of_1:
        fixed_groups.remove(group)
        groups_of_1.remove(group)
        if group["manager"] in active_students:
            unassigned_students.append(group["manager"])
            continue
        elif group["skeptic"] in active_students:
            unassigned_students.append(group["skeptic"])
            continue
        elif group["experimentalist"] in active_students:
            unassigned_students.append(group["experimentalist"])
            continue
        elif group["archivist"] in active_students:
            unassigned_students.append(group["archivist"])
            continue

    if len(groups_of_2) > len(unassigned_students):
        # destroy all groups of 2
        for group in groups_of_2:
            fixed_groups.remove(group)
            groups_of_2.remove(group)
            if group["manager"] in active_students:
                unassigned_students.append(group["manager"])
            if group["skeptic"] in active_students:
                unassigned_students.append(group["skeptic"])
            if group["experimentalist"] in active_students:
                unassigned_students.append(group["experimentalist"])
            if group["archivist"] in active_students:
                unassigned_students.append(group["archivist"])
    else:
        # assign all groups of 2 to have at least 3!
        for group in groups_of_2:
            new_member = unassigned_students.pop()
            fixed_groups.remove(group)
            groups_of_2.remove(group)
            if group["manager"] not in active_students:
                group["manager"] = new_member
                groups_of_3.append(group)
                fixed_groups.append(group)
                continue
            if group["skeptic"] not in active_students:
                group["skeptic"] = new_member
                groups_of_3.append(group)
                fixed_groups.append(group)
                continue
            if group["experimentalist"] not in active_students:
                group["experimentalist"] = new_member
                groups_of_3.append(group)
                fixed_groups.append(group)
                continue
            if group["archivist"] not in active_students:
                group["archivist"] = new_member
                groups_of_3.append(group)
                fixed_groups.append(group)
                continue

    for group in groups_of_3:
        if len(unassigned_students) > 0:
            new_member = unassigned_students.pop()
            groups_of_3.remove(group)
            fixed_groups.remove(group)
            if group["manager"] not in active_students:
                group["manager"] = new_member
                groups_of_4.append(group)
                fixed_groups.append(group)
                continue
            if group["skeptic"] not in active_students:
                group["skeptic"] = new_member
                groups_of_4.append(group)
                fixed_groups.append(group)
                continue
            if group["experimentalist"] not in active_students:
                group["experimentalist"] = new_member
                groups_of_4.append(group)
                fixed_groups.append(group)
                continue
            if group["archivist"] not in active_students:
                group["archivist"] = new_member
                groups_of_4.append(group)
                fixed_groups.append(group)
                continue

    if len(unassigned_students) == 3:
        # create a group of 3
        students_in_group = []
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        group = createGroup(students_in_group)
        fixed_groups.append(group)
    elif len(unassigned_students) == 4:
        # create a group of 4
        students_in_group = []
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        group = createGroup(students_in_group)
        fixed_groups.append(group)

    # assign archivist to needed role
    for group in fixed_groups:
        if group["archivist"]["name"] != "None":
            if group["manager"]["name"] == "None":
                group["manager"] = group["archivist"]
                group["archivist"] = {"name": "None"}
            elif group["skeptic"]["name"] == "None":
                group["skeptic"] = group["archivist"]
                group["archivist"] = {"name": "None"}
            elif group["experimentalist"]["name"] == "None":
                group["experimentalist"] = group["archivist"]
                group["archivist"] = {"name": "None"}

    groups = fixed_groups

    unassigned_students = []
    for student in active_students:
        present = False
        for group in groups:
            if group["manager"]["name"] == student["name"]:
                present = True
                break
            elif group["skeptic"]["name"] == student["name"]:
                present = True
                break
            elif group["experimentalist"]["name"] == student["name"]:
                present = True
                break
            elif group["archivist"]["name"] == student["name"]:
                present = True
                break
        if not present:
            unassigned_students.append(student)
    if len(unassigned_students) > 0:
        print("some students left unassigned, might need to reshuffle or manually fix")


def printGroups():
    global groups
    i = 1
    for group in groups:
        group_message = ""
        if (
            group["manager"]["name"] == "None"
            or group["skeptic"]["name"] == "None"
            or group["experimentalist"]["name"] == "None"
        ):
            group_message = "(Missing Roles!)"
        print("")
        print("Group %s %s" % (i, group_message))
        print("Manager: %s" % group["manager"]["name"])
        print("Experimentalist: %s" % group["experimentalist"]["name"])
        print("Theorist: %s" % group["skeptic"]["name"])
        print("Archivist: %s" % group["archivist"]["name"])
        i += 1
    unassigned_students = []
    for student in active_students:
        present = False
        for group in groups:
            if group["manager"]["name"] == student["name"]:
                present = True
                break
            elif group["skeptic"]["name"] == student["name"]:
                present = True
                break
            elif group["experimentalist"]["name"] == student["name"]:
                present = True
                break
            elif group["archivist"]["name"] == student["name"]:
                present = True
                break
        if not present:
            unassigned_students.append(student)
    print("")
    print("Unassigned")
    if len(unassigned_students) == 0:
        print("None")
    else:
        for student in unassigned_students:
            print(student["name"])


def swapStudents(id1):
    global groups
    selected_student_1 = None
    for student in all_students:
        if student["name"] == id or student["number"] == id:
            selected_student_1 = student
            break
    id2 = input("What student are you swapping with?")
    selected_student_2 = None
    for student in all_students:
        if student["name"] == id2 or student["number"] == id2:
            selected_student_2 = student
            break

    if selected_student_1 is None or selected_student_2 is None:
        print("invalid students")
    else:
        selected_student_1["swap"] = True
        selected_student_2["swap"] = True
        # hasattr(a, 'property')
        new_groups = copy.deepcopy(groups)
        swap = 0
        # swap student 1 with 2
        for group in new_groups:
            if group["manager"]["name"] == selected_student_1["name"]:
                group["manager"] = selected_student_2
                swap += 1
                break
            elif group["skeptic"]["name"] == selected_student_1["name"]:
                group["skeptic"] = selected_student_2
                swap += 1
                break
            elif group["experimentalist"]["name"] == selected_student_1["name"]:
                group["experimentalist"] = selected_student_2
                swap += 1
                break
            elif group["archivist"]["name"] == selected_student_1["name"]:
                group["archivist"] = selected_student_2
                swap += 1
                break
        # swap student 2 with 1
        for group in new_groups:
            if (
                group["manager"]["name"] == selected_student_2["name"]
                and "swap" not in group["manager"]
            ):
                group["manager"] = selected_student_1
                swap += 1
                break
            elif (
                group["skeptic"]["name"] == selected_student_2["name"]
                and "swap" not in group["skeptic"]
            ):
                group["skeptic"] = selected_student_1
                swap += 1
                break
            elif (
                group["experimentalist"]["name"] == selected_student_2["name"]
                and "swap" not in group["experimentalist"]
            ):
                group["experimentalist"] = selected_student_1
                swap += 1
                break
            elif (
                group["archivist"]["name"] == selected_student_2["name"]
                and "swap" not in group["archivist"]
            ):
                group["archivist"] = selected_student_1
                swap += 1
                break
        if swap == 2:
            # delete the swap attribute
            for group in new_groups:
                if hasattr(group["manager"], "swap"):
                    del group["manager"]["swap"]
                if hasattr(group["skeptic"], "swap"):
                    del group["skeptic"]["swap"]
                if hasattr(group["experimentalist"], "swap"):
                    del group["experimentalist"]["swap"]
                if hasattr(group["archivist"], "swap"):
                    del group["archivist"]["swap"]
            groups = new_groups
        else:
            print("at least one of these students wasn't actually assigned")


did_save = False


def saveAssignments():
    global groups
    global did_save
    for group in groups:
        for student in all_students:
            if group["manager"]["name"] == student["name"]:
                student["manager"] += 1
            elif group["skeptic"]["name"] == student["name"]:
                student["skeptic"] += 1
            elif group["experimentalist"]["name"] == student["name"]:
                student["experimentalist"] += 1
            elif group["archivist"] and group["archivist"]["name"] == student["name"]:
                student["archivist"] += 1

    for student in all_students:
        present = False
        for active_student in active_students:
            if active_student["name"] == student["name"]:
                student["present_days"] += 1
                present = True
                break
        if not present:
            student["absent_days"] += 1
    with open(filepath, "w+") as json_file:
        json.dump({"students": all_students}, json_file)
    did_save = True


assignStudentsToGroups()  # initially create groups
while True:  # main loop
    raw = input(
        "Is someone not here (n) or here now (h), and what is their name? Or simply try to fix groups (f), completely reshuffle groups (r), print a list of students (l), print group assignments (p), save assignments into json (save), swap student assignments (x), exit (exit)?"
    )
    raw = raw.split(" ")
    id = ""
    if len(raw) == 1:
        id = ""
    else:
        for i in range(0, len(raw)):
            if i > 0:
                id += raw[i]
                id += " "
        id = id[:-1]
    command = raw[0]

    if command == "n":
        selected_student = None
        for student in all_students:
            if student["name"] == id or student["number"] == id:
                selected_student = student
                break
        if selected_student is None:
            print("No student found with that name or number: %s" % id)
            continue
        # remove student from current groups
        for student in active_students:
            if student["name"] == selected_student["name"]:
                active_students.remove(student)
                break
        for group in groups:
            if group["manager"]["name"] == selected_student["name"]:
                group["manager"]["name"] = "None"
                break
            elif group["skeptic"]["name"] == selected_student["name"]:
                group["skeptic"]["name"] = "None"
                break
            elif group["experimentalist"]["name"] == selected_student["name"]:
                group["experimentalist"]["name"] = "None"
                break
            elif group["archivist"]["name"] == selected_student["name"]:
                group["archivist"]["name"] = "None"
                break
    elif command == "h":
        selected_student = None
        for student in all_students:
            if student["name"] == id or student["number"] == id:
                selected_student = student
                break
        if selected_student is None:
            print("No student found with that name or number")
            continue
        # add student back to present students
        active_students.append(selected_student)
    elif command == "x":
        swapStudents(id)
    elif command == "r":
        # reshuffle groups
        assignStudentsToGroups()
    elif command == "save":
        answer = input("Are you sure you're ready to save? (yes/no)")
        if answer == "yes":
            saveAssignments()
    elif command == "p":
        printGroups()
    elif command == "f":
        fixGroups()
    elif command == "l":
        listStudents()
    elif command == "exit":
        if did_save:
            print("bye")
            exit()
        else:
            answer = input(
                "You haven't saved yet, are you sure you want to exit? (yes/no)"
            )
            if answer == "yes":
                print("bye")
                exit()
    else:
        print("invalid command")
        continue
