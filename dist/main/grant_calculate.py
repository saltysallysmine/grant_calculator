from pprint import pprint
from dataclasses import dataclass

# app = Flask(__main__)

# webbrowser.open('https://google.com', new=2)

@dataclass
class Participant:
    name: str = 'Unknown'
    points: int = 0
    requested_grant: int = 0
    participates: bool = True
    calculated_grant: int = 0
    granted_grant: int = 0
    grant_without_distribution: int = 0
    grants_delta: int = 0


BUDGET = None
PARTICIPANTS = None
POINTS_SUM = None
REMAINDER = None
MIN_POINTS = None


def set(budget : int, participants_info : list):
    global BUDGET
    BUDGET = budget

    global PARTICIPANTS, POINTS_SUM, MIN_POINTS
    PARTICIPANTS = []
    POINTS_SUM = 0

    for participant in participants_info:
        name, points, requested_grant = participant
        PARTICIPANTS.append(Participant(name, points, requested_grant))

        POINTS_SUM += points

    MIN_POINTS = POINTS_SUM // len(participants_info)

    for x in PARTICIPANTS:
        x.participates = x.points > MIN_POINTS

    # pprint(PARTICIPANTS)


def calculate():
    global BUDGET, PARTICIPANTS, POINTS_SUM, REMAINDER

    REMAINDER = 0

    needing_addition = []

    for i, participant in enumerate(PARTICIPANTS):
        if participant.participates:
            points = participant.points 
            request = participant.requested_grant

            grant = round((BUDGET / POINTS_SUM) * points, 2)
            # print(grant)

            participant.calculated_grant = grant

            if grant > request:
                REMAINDER += grant - request
                participant.grants_delta = grant - request
                grant = request        
            
            elif grant < request:
                needing_addition.append(i)

            participant.grant_without_distribution = grant

            participant.granted_grant = grant
    

    while REMAINDER >= 0.01 and needing_addition != []:
        remainder_part = REMAINDER / len(needing_addition)

        for ind in needing_addition:
            PARTICIPANTS[ind].granted_grant += remainder_part

            REMAINDER -= remainder_part

            if PARTICIPANTS[ind].granted_grant >= PARTICIPANTS[ind].requested_grant:
                REMAINDER += PARTICIPANTS[ind].granted_grant - PARTICIPANTS[ind].requested_grant
                PARTICIPANTS[ind].granted_grant = PARTICIPANTS[ind].requested_grant
                needing_addition.pop(ind)

        print(needing_addition)
        print(REMAINDER)


if __name__ == '__main__':    
    pprint('Grant calculating script')