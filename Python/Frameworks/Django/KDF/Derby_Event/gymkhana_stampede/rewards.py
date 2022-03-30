from KDF.Derby_Event.models import Checkpoint, Event, Reward

if Checkpoint.isValid:
    Reward.point_total += Event.point_value
else:
    print("Your Current Point Total: ", Reward.point_total)
