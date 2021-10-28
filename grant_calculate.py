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


def set_conf(budget : int, participants_info : list):
    global BUDGET
    BUDGET = budget

    global PARTICIPANTS, POINTS_SUM, MIN_POINTS
    PARTICIPANTS = []
    POINTS_SUM = 0

    for participant in participants_info:
        name, points, requested_grant = participant
        PARTICIPANTS.append(Participant(name, points, requested_grant))

        POINTS_SUM += points

    # print(POINTS_SUM)
    # print()
    # MIN_POINTS = round(POINTS_SUM / len(participants_info))
    # print(MIN_POINTS)
    MIN_POINTS = 12
    POINTS_SUM = 772

    for x in PARTICIPANTS:
        x.participates = x.points >= MIN_POINTS

    # pprint(PARTICIPANTS)


def calculate():
    global BUDGET, PARTICIPANTS, POINTS_SUM, REMAINDER

    REMAINDER = BUDGET

    needing_addition = []

    for i, participant in enumerate(PARTICIPANTS):
        if participant.participates:
            points = participant.points 
            request = participant.requested_grant

            grant = round((BUDGET / POINTS_SUM) * points, 2)
            # print(grant)

            participant.calculated_grant = grant

            REMAINDER -= min(grant, request)
            if grant >= request:
                participant.grants_delta = round(grant - request, 2)
                grant = request
            else:
                needing_addition.append(i)

            participant.grant_without_distribution = grant

            participant.granted_grant = grant
    
    while REMAINDER >= 0.01 and needing_addition != []:
        needing_addition = list(filter(lambda x: x != -1, needing_addition))
        if not needing_addition:
            break
        remainder_part = REMAINDER / len(needing_addition)

        for i in range(len(needing_addition)):
            ind = needing_addition[i]
            PARTICIPANTS[ind].granted_grant += remainder_part

            REMAINDER -= remainder_part

            if PARTICIPANTS[ind].granted_grant >= PARTICIPANTS[ind].requested_grant:
                REMAINDER += PARTICIPANTS[ind].granted_grant - PARTICIPANTS[ind].requested_grant
                PARTICIPANTS[ind].granted_grant = PARTICIPANTS[ind].requested_grant

                pprint(needing_addition)
                pprint(ind)

                needing_addition[i] = -1

        print(needing_addition)
        print(REMAINDER)
    

def calculate_from_file():
    with open('inform.txt', 'r', encoding='utf-8') as fp:
        lines = list(map(lambda x: x.rstrip('\n'), fp.readlines()))
        parts = lines[1:]
        parts = zip(parts[::3], tuple(map(int, parts[1::3])), tuple(map(int, parts[2::3])))
        parts = list(parts)
        set_conf(int(lines[0]), parts)    
        calculate()


if __name__ == '__main__':    
    pprint('Grant calculating script')
