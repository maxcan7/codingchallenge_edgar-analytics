This is a work in progress for my insight data engineering 2019A session coding challenge 1.

It uses a bash shell script to pass arguments to a python script. The arguments should be the path for the input log, the inactivity period text file, and the sessionization output text file.

It uses the numpy package (and specifically genfromtxt) and the datetime package.

It currently does not account for sessions from the same IP separated by the inactivity period threshold, and it is not sorted by datetimes (currently sorted by IP).

Currently the test suite has not been implemented.

Currently it has only been tested with a log containing a single date, but in theory it should be able to accomodate differing dates, although this has not been tested.
