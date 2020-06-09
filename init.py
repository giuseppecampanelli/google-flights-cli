import click
import json

from flight_finder import FlightFinder

@click.command()
@click.option("--from", "-f", "from_", required=True, help="The departure airport.")
@click.option("--to", "-t", "to_", required=True, help="The arrival airport.")
@click.option("--start", "-s", "start_", required=True, help="The departure date.")
@click.option("--end", "-e", "end_", help="The arrival date.")
@click.option("--stops", "-c", "stops_", help="The maximum amount of stops.")

def find_flight(from_, to_, start_, end_, stops_):
    ff = FlightFinder(from_, to_, start_, end_, stops_)
    
    result = ff.find_flights()

    print(result)

    return result

if __name__ == '__main__':
    find_flight()
