import eyesweb_mobile
from patches_manager import *

# More input should be add to make the human motion "interactive" with the system
def movement(t, traj, patch, prev_position):
    length = len(traj)
    speed = 10
    # decisions can be added here

    next_position = traj[int(t/speed)%length - 1]
    if next_position != prev_position:
        print 'Move to coordinate X= ' + str(next_position)
        prev_position = next_position
    patch.set_block_parameter('HumanPosition', 'x_parameter', eyesweb_mobile.double_parameter(next_position))

    return next_position
