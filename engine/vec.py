from pygame import Vector2 as pg_vec2, Vector3 as pg_vec3


class Vec2(pg_vec2):
    def __add__(self, other):
        if type(other) in [int, float]:
            return Vec2(self.x + other, self.y + other)
        else:
            return Vec2(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if type(other) in [int, float]:
            return Vec2(self.x - other, self.y - other)
        else:
            return Vec2(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if type(other) in [int, float]:
            return Vec2(self.x * other, self.y * other)
        else:
            return Vec2(self.x * other[0], self.y * other[1])

    def __truediv__(self, other):
        if type(other) in [int, float]:
            return Vec2(self.x / other, self.y / other)
        else:
            return Vec2(self.x / other[0], self.y / other[1])

    def __floordiv__(self, other):
        if type(other) in [int, float]:
            return Vec2(self.x // other, self.y // other)
        else:
            return Vec2(self.x // other[0], self.y // other[1])

    def clamp(self, minn, maxn):
        return Vec2(max(min(self.x, maxn), minn), max(min(self.y, maxn), minn))


class Vec3(pg_vec3):
    def __add__(self, other):
        if type(other) in [int, float]:
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            return Vec3(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        if type(other) in [int, float]:
            return Vec3(self.x - other, self.y - other, self.z - other)
        else:
            return Vec3(self.x - other[0], self.y - other[1], self.z - other[2])

    def __mul__(self, other):
        if type(other) in [int, float]:
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            return Vec3(self.x * other[0], self.y * other[1], self.z * other[2])

    def __truediv__(self, other):
        if type(other) in [int, float]:
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            return Vec3(self.x / other[0], self.y / other[1], self.z / other[2])

    def __floordiv__(self, other):
        if type(other) in [int, float]:
            return Vec3(self.x // other, self.y // other, self.z // other)
        else:
            return Vec3(self.x // other[0], self.y // other[1], self.z // other[2])

    def clamp(self, minn, maxn):
        return max(min(self.x, maxn), minn), max(min(self.y, maxn), minn), max(min(self.z, maxn), minn)
