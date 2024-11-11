import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from US_visa.exception import USvisaException
from US_visa.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.Certified:int=1
        self.Denied:int=0

    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))