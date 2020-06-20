import click
import json

from flight_finder import FlightFinder

@click.command()
@click.option("--from", "-f", "from_", required=True, help="The departure airport.")
@click.option("--to", "-t", "to_", required=True, help="The arrival airport.")
@click.option("--start", "-s", "start_", required=True, help="The departure date.")
@click.option("--end", "-e", "end_", help="The arrival date.")
@click.option("--passengers", "-p", "passengers_", type=int, help="The amount of passengers.")
@click.option("--stops", "-c", "stops_", type=int, help="The maximum amount of stops.")
@click.option('--cheapest', "cheapest_", is_flag=True)

def search(from_, to_, start_, end_, passengers_, stops_, cheapest_):
    ff = FlightFinder(from_, to_, start_, end_, passengers_, stops_)
    
    if cheapest_:
        result = ff.find_flight()
    else:
        result = ff.find_flights()
    
    print(result)

if __name__ == '__main__':
    search()
