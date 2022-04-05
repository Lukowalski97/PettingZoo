import numpy as np


class SensingEnvironment:
    def __init__(self, sensors, width=5, length=5, check_range=2):
        self.width = width
        self.length = length
        self.sensors = sensors
        self.check_range = check_range

    def get_area(self):
        return self.width * self.length

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_sensors(self):
        return self.sensors.items()

    def get_sensor(self, id):
        return self.sensors[id]

    def remove_sensor(self, sensor):
        self.sensors.pop(sensor.id)

    def get_coverage_for_sensor_area(self, sensor):
        '''
        :returns 2D array bool array where True means positions covered by sensor of given sensor_id
        '''
        sensing_range = sensor.sensing_range
        (xx, yy) = np.ogrid[:self.width, :self.length]
        dist_from_center = np.sqrt((xx - sensor.x) ** 2 + (yy - sensor.y) ** 2)
        covered_area = dist_from_center <= sensing_range
        return covered_area

    def get_sensing_coverage_area(self):
        '''
        :returns 2D array bool array where True means positions covered by some sensor
        '''
        return self.get_coverage_excluding_sensor_area()

    def get_coverage_excluding_sensor_area(self, sensor=None):
        sensor_id = None
        if sensor is not None:
            sensor_id = sensor.id

        covered_area = np.full((self.width, self.length), False)
        for sensor in self.sensors.values():
            if sensor.id != sensor_id:
                area = self.get_coverage_for_sensor_area(sensor)
                for ind_y, row in enumerate(area):
                    for ind_x, x in enumerate(row):
                        if x and area[ind_y, ind_x]:
                            covered_area[(ind_x, ind_y)] = True
        return covered_area

    def get_coverage_by_other_sensors_area(self, sensor):
        check_range = self.check_range
        (xx, yy) = np.ogrid[:self.width, :self.length]
        dist_from_center = np.sqrt((xx - sensor.x) ** 2 + (yy - sensor.y) ** 2)
        covered_area = dist_from_center <= check_range

        result = np.full((self.width, self.length), False)
        for ind_y, row in enumerate(self.get_coverage_excluding_sensor_area(sensor)):
            for ind_x, x in enumerate(row):
                if x and covered_area[ind_y, ind_x]:
                    result[ind_x, ind_y] = True
        return result

    def get_covered_by_other_sensors(self, sensor):
        return self.__get_covered_for_array(self.get_coverage_by_other_sensors_area(sensor))

    def get_covered_area(self):
        coverage = self.get_sensing_coverage_area()
        return self.__get_covered_for_array(coverage)

    def get_covered_area_for_sensor(self, sensor):
        return self.__get_covered_for_array(self.get_coverage_for_sensor_area(sensor))

    def __get_covered_for_array(self, arr):
        covered_fields = 0
        for x in arr:
            for y in x:
                if y:
                    covered_fields += 1
        return covered_fields
