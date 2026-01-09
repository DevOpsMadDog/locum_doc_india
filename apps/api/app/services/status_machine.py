from app.models.enums import AssignmentStatus, ShiftStatus


SHIFT_TRANSITIONS = {
    ShiftStatus.draft: {ShiftStatus.posted},
    ShiftStatus.posted: {ShiftStatus.booked, ShiftStatus.canceled},
    ShiftStatus.booked: {ShiftStatus.en_route, ShiftStatus.canceled},
    ShiftStatus.en_route: {ShiftStatus.checked_in, ShiftStatus.no_show},
    ShiftStatus.checked_in: {ShiftStatus.completed},
    ShiftStatus.completed: {ShiftStatus.paid},
    ShiftStatus.paid: set(),
    ShiftStatus.canceled: set(),
    ShiftStatus.no_show: set(),
}

ASSIGNMENT_TRANSITIONS = {
    AssignmentStatus.pending: {AssignmentStatus.accepted, AssignmentStatus.canceled},
    AssignmentStatus.accepted: {AssignmentStatus.en_route, AssignmentStatus.canceled},
    AssignmentStatus.en_route: {AssignmentStatus.checked_in},
    AssignmentStatus.checked_in: {AssignmentStatus.completed},
    AssignmentStatus.completed: set(),
    AssignmentStatus.canceled: set(),
}


def can_transition_shift(current: ShiftStatus, target: ShiftStatus) -> bool:
    return target in SHIFT_TRANSITIONS.get(current, set())


def can_transition_assignment(current: AssignmentStatus, target: AssignmentStatus) -> bool:
    return target in ASSIGNMENT_TRANSITIONS.get(current, set())
