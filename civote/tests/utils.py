def finish_round(event):
    round = event.rounds.first()
    round.accepting_entries = False
    round.accepting_votes = True
    round.save()
    return round
