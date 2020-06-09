class FlightData:
    _from: str
    _to: str
    _start: str
    _end: str
    _airlines: []
    _price: int
    _connections: []
    _url: str

    def __init__(self, _from, _to, _start, _url, _end=None, _airlines=None, _price=None, _connections=None,):
        self._from = _from
        self._to = _to
        self._start = _start
        self._end = _end
        self._airlines = _airlines
        self._price = _price
        self._connections = _connections
        self._url = _url
    
    def set_from(self, _from):
        self._from = _from

    def set_to(self, _to):
        self._to = _to
    
    def set_start(self, _start):
        self._start = _start

    def set_end(self, _end):
        self._end = _end

    def set_airlines(self, _airlines):
        self._airlines = _airlines

    def set_price(self, _price):
        self._price = _price

    def set_connections(self, _connections):
        self._connections = _connections

    def set_url(self, _url):
        self._url = _url
    
    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_airlines(self):
        return self._airlines
    
    def get_price(self):
        return self._price

    def get_connections(self):
        return self._connections

    def get_url(self):
        return self._url
