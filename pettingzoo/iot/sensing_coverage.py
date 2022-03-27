from gym.spaces import Discrete

from pettingzoo.utils import ParallelEnv


class parallel_env(ParallelEnv):
    def __init__(self, env, max_sensing_range=5):
        self.env = env
        self.max_sensing_range = max_sensing_range

    def render(self, mode="human"):
        print(self.env.get_covered_area())
        print(self.env.get_sensing_coverage())

    def step(self, actions):
        pass
        # TODO VERY MUCH

    def observation_space(self, agent):
        pass
        # TODO

    def action_space(self, agent):
        return Discrete(self.max_sensing_range * 2 + 1)


class Sensor:
    def __init__(self, id, x, y, sensing_range=0, max_sensing_range=5):
        self.id = id
        self.x = x
        self.y = y
        self.max_sensing_range = max_sensing_range
        self.sensing_range = sensing_range

    def adjust_sensing_range(self, diff):
        new_sensing_range = self.sensing_range + diff
        if 0 <= new_sensing_range <= self.max_sensing_range:
            self.sensing_range = new_sensing_range


class SensingEnvironment:
    def __init__(self, sensors, width=5, length=5, check_range=2):
        self.width = width
        self.length = length
        self.sensors = sensors
        self.check_range = check_range

    def get_sensors(self):
        return self.sensors

    def get_sensing_area_for_sensor(self, sensor_id):
        '''
        :returns array of tuples (x,y) which indicates positions in area which are covered by sensor of given sensor_id
        '''
        sensor = self.sensors[sensor_id]
        sensing_range = sensor.sensing_range
        (start_x, start_y) = (sensor.x - sensing_range, sensor.y - sensing_range)
        (end_x, end_y) = (sensor.x + sensing_range, sensor.y + sensing_range)
        covered_area = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if self.__is_valid_position(x, y):
                    covered_area.append((x, y))
        return covered_area

    def get_sensing_coverage(self):
        '''
        :returns 2D array bool array where True means positions covered by some sensor
        '''
        return self.get_sensing_coverage_excluding_sensor()

    def get_sensing_coverage_excluding_sensor(self, sensor_id=None):
        covered_area = [[False for _ in range(self.width + 1)] for _ in range(self.length + 1)]
        for sensor in self.sensors.values():
            if sensor.id != sensor_id:
                area = self.get_sensing_area_for_sensor(sensor.id)
                for position in area:
                    covered_area[position[0]][position[1]] = True

        return covered_area

    def get_covered_by_other_sensors_area(self, sensor):
        (start_x, start_y) = (sensor.x - self.check_range, sensor.y - self.check_range)
        (end_x, end_y) = (sensor.x + self.check_range, sensor.y + self.check_range)
        if start_x < 0:
            start_x = 0
        if start_y < 0:
            start_y = 0
        if end_x > self.width:
            end_x = self.width
        if end_y > self.length:
            end_y = self.length
        new_arr = []
        for x in self.get_sensing_coverage_excluding_sensor(sensor.id)[start_x:end_x + 1]:
            new_arr.append(x[start_y:end_y + 1])
        return new_arr

    def get_covered_area(self):
        covered_fields = 0
        coverage = self.get_sensing_coverage()
        for x in coverage:
            for y in x:
                if y:
                    covered_fields += 1
        return covered_fields

    def get_covered_area_for_sensor(self, sensor_id):
        return len(self.get_sensing_area_for_sensor(sensor_id))

    def __is_valid_position(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.length


if __name__ == '__main__':
    sensor0 = Sensor(0, 1, 1, 2)
    sensor1 = Sensor(1, 2, 5, 2)
    sensor2 = Sensor(2, 4, 4, 2)
    sensors = {0: sensor0, 1: sensor1, 2: sensor2}
    env = SensingEnvironment(sensors, 5, 5)
    print(env.get_covered_area())
    print(env.get_sensing_coverage())
    print(env.get_covered_by_other_sensors_area(sensor0))
