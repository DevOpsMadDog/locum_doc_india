from app.models.enums import AssignmentStatus, ShiftStatus
from app.services.status_machine import can_transition_assignment, can_transition_shift


def test_shift_transitions():
    assert can_transition_shift(ShiftStatus.draft, ShiftStatus.posted)
    assert not can_transition_shift(ShiftStatus.draft, ShiftStatus.booked)
    assert can_transition_shift(ShiftStatus.posted, ShiftStatus.booked)
    assert can_transition_shift(ShiftStatus.booked, ShiftStatus.en_route)
    assert not can_transition_shift(ShiftStatus.completed, ShiftStatus.booked)


def test_assignment_transitions():
    assert can_transition_assignment(AssignmentStatus.pending, AssignmentStatus.accepted)
    assert not can_transition_assignment(AssignmentStatus.pending, AssignmentStatus.completed)
    assert can_transition_assignment(AssignmentStatus.accepted, AssignmentStatus.en_route)
