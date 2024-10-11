
    # Student Class
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return self.name


# Group Class
class Group:
    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name
        self.members = set()  # Use a set to avoid duplicate members

    def add_member(self, student):
        """Add a student to the group"""
        self.members.add(student)

    def remove_member(self, student):
        """Remove a student from the group"""
        self.members.remove(student)

    def show_members(self):
        """Return a list of member names"""
        return [str(student) for student in self.members]


# Action Class to Track Registrations/Unregistrations
class Action:
    def __init__(self, action_type, group, student):
        self.action_type = action_type  # "register" or "unregister"
        self.group = group
        self.student = student


# StudyGroupScheduler Class with Undo Stack
class StudyGroupScheduler:
    def __init__(self):
        self.groups = {}  # group_id -> Group object
        self.students = {}  # student_id -> Student object
        self.undo_stack = []  # Stack for undo operations

    def create_group(self, group_id, group_name):
        """Create a new group"""
        if group_id not in self.groups:
            self.groups[group_id] = Group(group_id, group_name)
            print(f"Group '{group_name}' created.")
        else:
            print("Group already exists")

    def create_student(self, student_id, name):
        """Create a new student"""
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
            print(f"Student '{name}' created.")
        else:
            print("Student already exists.")

    def list_groups(self):
        """List all available groups"""
        if not self.groups:
            print("No groups available.")
        else:
            print("\nAvailable Groups:")
            for group_id, group in self.groups.items():
                print(f"Group ID: {group_id}, Name: {group.group_name}")
        print()

    def list_students(self):
        """List all available students"""
        if not self.students:
            print("No students available.")
        else:
            print("\nAvailable Students:")
            for student_id, student in self.students.items():
                print(f"Student ID: {student_id}, Name: {student.name}")
        print()

    def register_student(self):
        """Register a student to a group"""
        if not self.groups:
            print("No groups available. Please create a group first.")
            return

        if not self.students:
            print("No students available. Please create a student first.")
            return

        # Show available groups
        self.list_groups()

        group_id = int(input("Enter Group ID to register student: "))
        if group_id not in self.groups:
            print("Invalid Group ID.")
            return

        # Show available students
        self.list_students()

        student_id = int(input("Enter Student ID to register: "))
        if student_id not in self.students:
            print("Invalid Student ID.")
            return

        group = self.groups[group_id]
        student = self.students[student_id]

        group.add_member(student)
        # Push the action to the stack for undo
        self.undo_stack.append(Action("register", group, student))
        print(f"Registered {student.name} to {group.group_name}.")

    def unregister_student(self, group_id, student_id):
        """Unregister a student from a group"""
        if group_id in self.groups and student_id in self.students:
            group = self.groups[group_id]
            student = self.students[student_id]
            if student in group.members:
                group.remove_member(student)
                # Push the action to the stack for undo
                self.undo_stack.append(Action("unregister", group, student))
                print(f"Unregistered {student.name} from {group.group_name}.")
            else:
                print(f"Student {student.name} is not in the group.")
        else:
            print("Invalid group ID or student ID.")

    def undo(self):
        """Undo the last register/unregister action"""
        if self.undo_stack:
            last_action = self.undo_stack.pop()  # Get the last action
            if last_action.action_type == "register":
                last_action.group.remove_member(last_action.student)
                print(f"Undo: Removed {last_action.student.name} from {last_action.group.group_name}")
            elif last_action.action_type == "unregister":
                last_action.group.add_member(last_action.student)
                print(f"Undo: Re-added {last_action.student.name} to {last_action.group.group_name}")
        else:
            print("No actions to undo.")

    def show_group_members(self, group_id):
        """Show members of a specific group"""
        if group_id in self.groups:
            group = self.groups[group_id]
            members = group.show_members()
            if members:
                print(f"Members of {group.group_name}: {', '.join(members)}")
            else:
                print(f"{group.group_name} has no members.")
        else:
            print("Group does not exist.")

    def show_all_groups(self):
        """Show all groups and their members"""
        if not self.groups:
            print("No groups available.")
        else:
            print("\nAll Groups and Their Members:")
            for group_id, group in self.groups.items():
                members = group.show_members()
                members_list = ', '.join(members) if members else 'No members'
                print(f"Group ID: {group_id}, Name: {group.group_name}, Members: {members_list}")
        print()


# Main function to interact with the user
def main():
    scheduler = StudyGroupScheduler()

    while True:
        print("\nStudy Group Scheduler")
        print("1. Create Group")
        print("2. Register Student to study")
        print("3. Registered Student to Group")
        print("4. Unregister Student from Group")
        print("5. Undo Last Action")
        print("6. Show All Groups with Members")
        print("7. Exit")
        choice = input("Choose an option 1-7: ")

        if choice == "1":
            group_id = int(input("Enter Group ID: "))
            group_name = input("Enter Group Name: ")
            scheduler.create_group(group_id, group_name)

        elif choice == "2":
            student_id = int(input("Enter Student ID: "))
            name = input("Enter Student Name: ")
            scheduler.create_student(student_id, name)

        elif choice == "3":
            scheduler.register_student()

        elif choice == "4":
            group_id = int(input("Enter Group ID: "))
            student_id = int(input("Enter Student ID: "))
            scheduler.unregister_student(group_id, student_id)

        elif choice == "5":
            scheduler.undo()

        elif choice == "6":
            scheduler.show_all_groups()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

