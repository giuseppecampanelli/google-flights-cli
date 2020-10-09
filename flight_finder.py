import json
import re

from flight_data import FlightData

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlightFinder:
    _from: str
    _to: str
    _start: str
    _end: str
    _stops: int
    _passengers: int
    _url: str

    def __init__(self, _from, _to, _start, _end=None, _passengers=None, _stops=None):
        
        ## Check from , to is not empty
        if not _from or len(_from.strip()) == 0:
            raise ValueError("From was empty")
        
        if not _to or len(_to.strip()) == 0:
            raise ValueError("To was empty")

        if _from.upper() == _to.upper() :
            raise ValueError("From and To must not same place")

        _from = _from.upper()
        _to   = _to.upper()

        ## Check start , date is not empty and input with format (YYYY-MM-DD)
        if not _start or len(_start.strip()) == 0:
            raise ValueError("Start was empty")
        else :
            try:
                datetime.strptime(_start, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect date format, it must be with YYYY-MM-DD")

        if not _end is None or len(_end.strip()) > 0:
            try:
                datetime.strptime(_end, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect date format, it must be with YYYY-MM-DD")
        
        ## Check start,end must be not less than today
        if datetime.strptime(_start, '%Y-%m-%d') < datetime.now() :
            raise ValueError("Start Date must be more than or equal Today")

        if not _end is None :
            if datetime.strptime(_end, '%Y-%m-%d') < datetime.now() :
                raise ValueError("End Date must be more than or equal Today")
        
        ## Check start,must more than end (in case : end is not None)
        if not _end is None :
            if not datetime.strptime(_start, '%Y-%m-%d') < datetime.strptime(_end, '%Y-%m-%d') :
                raise ValueError("End Date must be more than or equal Start")

        ## Check stop must be integer and > 0
        if not _stops is None :
            if not isinstance(_stops, int) :
                raise ValueError("Stop must be decimal")
            if int(_stops) < 0 :
                raise ValueError("Stop must be more than 0")

        ## Check passanger must be integer and > 0
        if not _passengers is None :
            if not isinstance(_passengers, int) :
                raise ValueError("Passanger must be decimal")
            if int(_passengers) < 1 :
                raise ValueError("Passanger must be more than 1")
                
        self._from = _from
        self._to = _to
        self._start = _start
        self._end = _end
        self._passengers = _passengers
        self._stops = _stops

        self.__generate_url()

    def __generate_url(self):
        self._url = "https://www.google.ca/flights#flt={}.{}.{}".format(self._from, self._to, self._start)

        if self._end:
            self._url += "*{}.{}.{}".format(self._to, self._from, self._end)

        if self._stops:
            self._url += ";s:{}*{}".format(self._stops, self._stops)

        if self._passengers:
            self._url += ";px:{}".format(self._passengers)

        if self._end:
            self._url += ";t:f"
        else:
            self._url += ";tt:o"

    def find_flight(self):
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.get(self._url)

        flights = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ol"))
        )

        flight = flights.find_element_by_css_selector("li")

        result = self.__get_flight_data(flight)

        driver.close()
        
        return json.dumps(result)

    def find_flights(self):
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.get(self._url)

        data = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ol"))
        )

        flights = data.find_elements_by_xpath("li")

        result = []

        for flight in flights:
            result.append(self.__get_flight_data(flight))

        driver.close()
        
        return json.dumps(result)
    
    def __get_flight_data(self, flight):
        flight_data = FlightData(self._from, self._to, self._start, self._url, _end=self._end, _passengers=self._passengers)
        
        price = flight.find_element_by_xpath("div/div[1]/div[2]/div[1]/div[1]/div[6]/div[1]").text
        flight_data.set_price(int(re.sub("[^0-9]", "", price)))

        airlines = flight.find_elements_by_xpath("div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/span[1]/span")
        airlines_list = []

        for airline in airlines:
            airline_spans = airline.find_elements_by_xpath("span")
            airlines_list.append(airline_spans[len(airline_spans)-1].text)
        
        flight_data.set_airlines(airlines_list)

        connections = flight.find_elements_by_xpath("div/div[1]/div[2]/div[1]/div[1]/div[4]/div[2]/span[1]/span")

        if connections:
            connections_list = []

            for connection in connections:
                connection_spans = connection.find_elements_by_xpath("span")
                connections_list.append(connection_spans[len(connection_spans)-1].text)
            
            flight_data.set_connections(connections_list)
        
        return json.dumps(flight_data.__dict__)
