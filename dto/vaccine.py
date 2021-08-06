from enum import Enum

class VaccineVendor(Enum):
    PFIZER = 'VEN00013'
    MODERNA = 'VEN00014'
    ASTRAZENECA = 'VEN00015'
    JANSSEN = 'VEN00016'
    ANY = 'ANY'

    @classmethod
    def values(cls):
        return map(lambda c: c.value, cls)