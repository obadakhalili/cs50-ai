class SolutionDNE(RuntimeError):
    def __init__(self):
        super().__init__("solution does not exist")


def backtrack(csp, assignments={}):
    unassigned_vars = csp.vars - assignments.keys()
    is_assignment_complete = not bool(unassigned_vars)

    if is_assignment_complete:
        return assignments

    var = unassigned_vars.pop()

    for value in csp.get_domain_of_var(var):
        if csp.is_assignment_consistent(var, value, assignments):
            assignments[var] = value
            try:
                return backtrack(csp, assignments)
            except SolutionDNE:
                del assignments[var]

    raise SolutionDNE()


class ExamSchedulingCSP:
    def __init__(self):
        self.vars = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
        ]
        # The procedures for maintaining node- and arc-consistency is performed on the following data sturcture
        self.courses_slots = {
            "A": ["Mon", "Tue", "Wed"],
            "B": ["Mon", "Tue", "Wed"],
            "C": ["Mon", "Tue", "Wed"],
            "D": ["Mon", "Tue", "Wed"],
            "E": ["Mon", "Tue", "Wed"],
            "F": ["Mon", "Tue", "Wed"],
            "G": ["Mon", "Tue", "Wed"],
        }
        self.constraints = {
            "A": ["B", "c"],
            "B": ["A", "C", "D", "E"],
            "C": ["A", "B", "E", "F"],
            "D": ["D", "E"],
            "E": ["C", "B", "D", "F", "G"],
            "F": ["C", "E", "G"],
            "G": ["F", "E"],
        }

    def get_domain_of_var(self, var):
        return self.courses_slots[var]

    def is_assignment_consistent(self, var, value, assignments):
        return not any(
            value == assignments[neighbor_var] if neighbor_var in assignments else False
            for neighbor_var in self.constraints[var]
        )


try:
    print(backtrack(ExamSchedulingCSP()))
except SolutionDNE as e:
    print(e)
