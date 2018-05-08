# Influencer Search
Using [com-Youtube](https://snap.stanford.edu/data/com-Youtube.html) as dataset, with 1.134.890 nodes and 2.987.624 edges.
Our goal is find the k users with highest influence, adopting local search (random-restart hill climbing) and two heuristics: number of friends and number of groups.

Implemented in [Python 3](https://www.python.org/).

**Parameters:**
* k: number of influencers to find
* heuristic_id: FRIENDS or GROUPS to choose which heuristic function to use

**Running:**
```
cd [...]/influencer_search/src
python main.py
```
