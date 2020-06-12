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
