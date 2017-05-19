#!/usr/bin/env python
import suds.client
import suds.cache
import zeep


LOCATIONS_SERVICE = 'http://localhost:8000/locationsService?wsdl'
ERROR_SERVICE = 'http://localhost:8000/errorService?wsdl'


class FakeService:
    def call_service(self):
        return self.client.service.getLocations({'maxRecords': 100})


class SudsService(FakeService):
    def __init__(self, wsdl):
        self.client = suds.client.Client(wsdl, cache=suds.cache.NoCache())


class ZeepService(FakeService):
    def __init__(self, wsdl):
        # Required strict=False because response is returned
        # as if it was from Apache Axis which does not preserve
        # the order the same as in the xsd
        try:
            self.client = zeep.Client(wsdl, strict=False)
        except TypeError:
            # Zeep is too old and do not support strict argument
            self.client = zeep.Client(wsdl)


if __name__ == '__main__':
    suds_client = SudsService(LOCATIONS_SERVICE)
    print("\nSuds locations response")
    print(suds_client.call_service())

    zeep_client = ZeepService(LOCATIONS_SERVICE)
    print("\nZeep locations response")
    print(zeep_client.call_service())

    suds_client = SudsService(ERROR_SERVICE)
    print("\nSuds error response")
    print(suds_client.call_service())

    zeep_client = ZeepService(ERROR_SERVICE)
    print("\nZeep Error response")
    print(zeep_client.call_service())
