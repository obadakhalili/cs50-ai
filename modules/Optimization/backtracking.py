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
