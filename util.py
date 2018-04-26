class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, imu_vector):
        return Vector3(
            x=self.x + imu_vector.x,
            y=self.y + imu_vector.y,
            z=self.z + imu_vector.z
        )

    def __sub__(self, imu_vector):
        return Vector3(
            x=self.x - imu_vector.x,
            y=self.y - imu_vector.y,
            z=self.z - imu_vector.z
        )

    def __truediv__(self, sample_num):
        return Vector3(
            x=self.x / sample_num,
            y=self.y / sample_num,
            z=self.z / sample_num
        )

    def dist(self, imu_vector):
        return Vector3(
            x=abs(self.x - imu_vector.x),
            y=abs(self.y - imu_vector.y),
            z=abs(self.z - imu_vector.z)
        )

    def __str__(self):
        return "{0},{1},{2}".format(self.x, self.y, self.z)

    @classmethod
    def from_imu_vector(cls, imu_vector):
        return cls(imu_vector[0], imu_vector[1], imu_vector[2])

def dist(curr, key):
    if key in SCALARS:
        return abs(curr - OFFSETS[key])
    else:
        return Vector3(
            x=abs(curr.x - OFFSETS[key].x),
            y=abs(curr.y - OFFSETS[key].y),
            z=abs(curr.z - OFFSETS[key].z)
        )
