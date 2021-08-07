import json

class Region:

    @classmethod
    def from_bytes(cls, bytes):
        region_json = json.loads(bytes.decode('utf-8'))
        top_left = (region_json['topLeft']['x'], region_json['topLeft']['y'])
        bottom_right = (region_json['bottomRight']['x'], region_json['bottomRight']['y'])
        return Region(top_left, bottom_right)

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def __str__(self):
        return "좌상 [{:.4f}, {:.4f}] 우하 [{:.4f}, {:.4f}]".format(*self.top_left, *self.bottom_right)

    def __eq__(self, other):
        if isinstance(other, Region):
            return (self.top_left == other.top_left) and (self.bottom_right == other.bottom_right)
        return False

    def convert_to_dto(self):
        return {
            "bottomRight": {
                "x": self.bottom_right[0], 
                "y": self.bottom_right[1]
            }, 
            "onlyLeft": False, 
            "order": "latitude",
            "topLeft": {
                "x": self.top_left[0], 
                "y": self.top_left[1]
            }
        }