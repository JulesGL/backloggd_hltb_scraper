# backloggd_hltb_scraper

This small project contains two `.py` files :

- `backloggd.py` can be executed to fetch your backlog on [Backloggd](https://www.backloggd.com/) and convert it to a csv file.
- `hltb.py` takes a csv file with game title and add the length to complete it according to [How Long to Beat](https://howlongtobeat.com/).

### Making it work

- Install the requirements
- Change your username and the `max_page` parameter in `backloggd.py`, corresponding to the number of page in your collection.
We could directly fetch it, but at the moment, it's not implemented.