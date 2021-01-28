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
        manager = {"manager": 100}
        experimentalist = {"experimentalist": 100}
        skeptic = {"skeptic": 100}
        archivist = {"name": "None", "archivist": 100}
        for student in students_in_group:
            if student["manager"] < manager["manager"]:
                manager = student
        for student in students_in_group:
            if (
                student["experimentalist"] < experimentalist["experimentalist"]
                and manager != student
            ):
                experimentalist = student
        for student in students_in_group:
            if (
                student["skeptic"] < skeptic["skeptic"]
                and manager != student
                and experimentalist != student
            ):
                skeptic = student
        for student in students_in_group:
            if skeptic != student and manager != student and experimentalist != student:
                archivist = student
                break

        group = {
            "manager": manager,
            "skeptic": skeptic,
            "experimentalist": experimentalist,
            "archivist": archivist,
        }
        groups.append(group)

    for i in range(0, int(num_of_3_groups)):
        # group of 3 logic
        students_in_group = []
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        students_in_group.append(students.pop())
        manager = {"manager": 100}
        experimentalist = {"experimentalist": 100}
        skeptic = {"skeptic": 100}
        for student in students_in_group:
            if student["manager"] < manager["manager"]:
                manager = student
        for student in students_in_group:
            if (
                student["experimentalist"] < experimentalist["experimentalist"]
                and manager != student
            ):
                experimentalist = student
        for student in students_in_group:
            if (
                student["skeptic"] < skeptic["skeptic"]
                and manager != student
                and experimentalist != student
            ):
                skeptic = student

        group = {
            "manager": manager,
            "skeptic": skeptic,
            "experimentalist": experimentalist,
            "archivist": {"name": "None", "archivist": 100},
        }
        groups.append(group)
    print("Groups Assigned")


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
        manager = {"manager": 100}
        experimentalist = {"experimentalist": 100}
        skeptic = {"skeptic": 100}
        for student in students_in_group:
            if student["manager"] < manager["manager"]:
                manager = student
        for student in students_in_group:
            if (
                student["experimentalist"] < experimentalist["experimentalist"]
                and manager != student
            ):
                experimentalist = student
        for student in students_in_group:
            if (
                student["skeptic"] < skeptic["skeptic"]
                and manager != student
                and experimentalist != student
            ):
                skeptic = student

        group = {
            "manager": manager,
            "skeptic": skeptic,
            "experimentalist": experimentalist,
            "archivist": {"name": "None", "archivist": 100},
        }
        fixed_groups.append(group)
    elif len(unassigned_students) == 4:
        # create a group of 4
        students_in_group = []
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        students_in_group.append(unassigned_students.pop())
        manager = {"manager": 100}
        experimentalist = {"experimentalist": 100}
        skeptic = {"skeptic": 100}
        archivist = {"name": "None", "archivist": 100}
        for student in students_in_group:
            if student["manager"] < manager["manager"]:
                manager = student
        for student in students_in_group:
            if (
                student["experimentalist"] < experimentalist["experimentalist"]
                and manager != student
            ):
                experimentalist = student
        for student in students_in_group:
            if (
                student["skeptic"] < skeptic["skeptic"]
                and manager != student
                and experimentalist != student
            ):
                skeptic = student
        for student in students_in_group:
            if skeptic != student and manager != student and experimentalist != student:
                archivist = student
                break

        group = {
            "manager": manager,
            "skeptic": skeptic,
            "experimentalist": experimentalist,
            "archivist": archivist,
        }
        fixed_groups.append(group)

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
        print("")
        print("Group %s" % i)
        print("Manager: %s" % group["manager"]["name"])
        print("Experimentalist: %s" % group["experimentalist"]["name"])
        print("Skeptic: %s" % group["skeptic"]["name"])
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


def saveAssignments():
    global groups
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


assignStudentsToGroups()  # initially create groups
while True:  # main loop
    raw = input(
        "Is someone not here (n) or here now (h), and what is their name or number? Or simply try to fix groups (f), completely reshuffle groups (r), print groups (p), save assignments into json(s), exit (exit)?"
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
        # add student back to current groups
        active_students.append(selected_student)
    elif command == "r":
        # reshuffle groups
        assignStudentsToGroups()
    elif command == "s":
        saveAssignments()
    elif command == "p":
        printGroups()
    elif command == "f":
        fixGroups()
    elif command == "exit":
        print("bye")
        exit()
    else:
        print("invalid command")
        continue

students = [
    {
        name: "Last,First",
        number: 0,  # just for easy identification
        manager: 0,
        skeptic: 0,
        experimentalist: 0,
        archivist: 0,
        present_days: 0,
        absent_days: 0,
    }
]

group = {
    archivist: studentObject,
    manager: studentObject,
    skeptic: studentObject,
    experimentalist: studentObject,
}


# # if we cant repair all groups of 2 destroy them
# if len(groups_of_2) > len(unassigned_students):
#     for group in groups_of_2:
#         fixed_groups.remove(group)
#         if group["manager"] in active_students:
#             unassigned_students.append(group["manager"])
#         elif group["skeptic"] in active_students:
#             unassigned_students.append(group["skeptic"])
#         elif group["experimentalist"] in active_students:
#             unassigned_students.append(group["experimentalist"])
#         elif group["archivist"] in active_students:
#             unassigned_students.append(group["archivist"])
#     groups_of_2 = []
# # fill in all groups of 2 to make them 3
# elif len(groups_of_2) > 0 and len(unassigned_students) > 0:
#     for i in range(0, len(groups_of_2)):
#         group = groups_of_2[i]
#         new_member = unassigned_students.pop()
#         members = [new_member]
#         if group["manager"] in active_students:
#             members.append(group["manager"])
#         if group["skeptic"] in active_students:
#             members.append(group["skeptic"])
#         if group["experimentalist"] in active_students:
#             members.append(group["experimentalist"])
#         if group["archivist"] in active_students:
#             members.append(group["archivist"])
#         # group of 3 logic
#         manager = {"manager": 100}
#         experimentalist = {"experimentalist": 100}
#         skeptic = {"skeptic": 100}
#         for student in members:
#             if student["manager"] < manager["manager"]:
#                 manager = student
#         for student in members:
#             if (
#                 student["experimentalist"] < experimentalist["experimentalist"]
#                 and manager != student
#             ):
#                 experimentalist = student
#         for student in members:
#             if (
#                 student["skeptic"] < skeptic["skeptic"]
#                 and manager != student
#                 and experimentalist != student
#             ):
#                 skeptic = student

#         group = {
#             "manager": manager,
#             "skeptic": skeptic,
#             "experimentalist": experimentalist,
#             "archivist": {"name": "None", "archivist": 100},
#         }

#         print("group of 2 made into group of 3: %s" % group)

#         fixed_groups.append(group)

# if len(groups_of_3) >= len(unassigned_students):
#     # we can solve this
#     for group in fixed_groups:
#         if group["archivist"]["name"] == "None":
#             student = unassigned_students.pop()
#             group["archivist"] = student
#             print("%s assigned to group as archivist" % student["name"])
#             if len(unassigned_students) == 0:
#                 break