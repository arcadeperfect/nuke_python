import math
import nuke

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def get_distance(a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

cam = nuke.selectedNode()
translate_knob = cam['translate']

t_x = translate_knob.animation(0)
t_y = translate_knob.animation(1)
t_z = translate_knob.animation(2)

first = int(t_x.keys()[0].x)
last = int(t_x.keys()[-1].x)

positions = []
times = []
distances = [0]
total_distance = 0

previous_p = Vec3(t_x.evaluate(first), t_y.evaluate(first), t_z.evaluate(first))
positions.append(previous_p)
times.append(first)

for frame in range(first + 1, last + 1):
    this_p = Vec3(t_x.evaluate(frame), t_y.evaluate(frame), t_z.evaluate(frame))
    d = Vec3.get_distance(previous_p, this_p)
    total_distance += d
    distances.append(total_distance)
    positions.append(this_p)
    times.append(frame)
    previous_p = this_p

# Calculate the average velocity
average_velocity = total_distance / (last - first)

# Create new time array where time change is inversely proportional to velocity
new_times = [first]
for i in range(1, len(times)):
    segment_distance = distances[i] - distances[i-1]
    segment_time = times[i] - times[i-1]
    segment_velocity = segment_distance / segment_time if segment_time != 0 else average_velocity
    time_factor = segment_velocity / average_velocity
    new_segment_time = segment_time * time_factor
    new_times.append(new_times[-1] + new_segment_time)

# Normalize new_times to fit within the original frame range
new_times = [first + (t - first) * (last - first) / (new_times[-1] - first) for t in new_times]


# Create lookup table
flatten = nuke.createNode("TimeWarp")
flatten['label'].setValue("flatten")

for original_time, new_time in zip(times, new_times):
    l = flatten["lookup"]
    l.setAnimated()
    flatten['lookup'].setValueAt(original_time, new_time)

apply = nuke.createNode("TimeWarp")
apply['label'].setValue("apply")

for original_time, new_time in zip(times, new_times):
    l = apply["lookup"]
    l.setAnimated()
    apply['lookup'].setValueAt(new_time,original_time)

