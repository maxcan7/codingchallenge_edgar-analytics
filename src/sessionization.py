def sessionization(*args):
    import csv
    import numpy as np
    from numpy import genfromtxt
    import datetime as dt

    # Separate input and output paths and variables into separate lists
    logpath = args[0]
    inactpath = args[1]
    sesspath = args[2]
        
    # Read in the inactivity period threshold
    with open(inactpath) as f:
        inactive = f.read()
        inactive = int(inactive)
        f.close()

    # Read data from log using numpy
    logdata = genfromtxt(logpath, delimiter=',', encoding="utf8", dtype=object, names=True)
    
    # Find unique IPs
    ip = np.unique(logdata['ip'])

    # Find the first request for each IP and set up sessions output array
    for i in ip:
        user = logdata[logdata['ip'] == i]
        for j in range(len(user)):
            if 'session' not in locals():
                session = np.array([user[j][0],user[j][1],user[j][2],'','',int(1),int(1)], dtype=object)
            else:
                session = np.vstack((session,np.array([user[j][0],user[j][1],user[j][2],'','',int(1),int(1)], dtype=object)))
                
    # Evaluate sessions by looping through ip, subset to datetime relative to inactivity threshold, and calculate 
    # end datetime, duration, and request count 
    for i in ip:
        # Find users with only one request
        if len(session[session[:,0] == i]) == 1:
            # Set end datetime == start datetime and write to output file
            session[session[:,0] == i,3] = session[session[:,0] == i,1]
            session[session[:,0] == i,4] = session[session[:,0] == i,2]
            sesh = session[session[:,0] == i]
            with open(sesspath, 'w', encoding='utf8') as outputfile:
                outputfile.write(','.join(sesh[0].astype(str)) + '\n')
        else:
            # Subset by IPs
            user = session[session[:,0] == i]
            # Loop through number of requests of an IP
            for u in range(len(user)):
                # Concatenate date and time for each requests and stack them into an array for all requests
                if 'user_datetimes' not in locals():
                    user_datetimes = np.hstack([user[u,1],user[u,2]])
                else:
                    user_datetimes = np.vstack((user_datetimes, np.hstack([user[u,1],user[u,2]])))
            # Convert date and time objects to string
            user_datetimes = user_datetimes.astype(str)
            # Concatenate date and time strings
            user_datetimes = np.apply_along_axis(lambda d: d[0] + ' ' + d[1], 1, user_datetimes)
            # Loop through each instance and convert datetime string to datetime object
            idx = 0
            for dtidx in user_datetimes:
                if idx == 0:
                    user_datetimes_obj = np.array([dt.datetime.strptime(dtidx, '%Y-%m-%d %H:%M:%S')])
                    idx += 1
                else:
                    user_datetimes_obj = np.vstack((user_datetimes_obj, [dt.datetime.strptime(dtidx, '%Y-%m-%d %H:%M:%S')]))
            # Delete the ith user_datetimes before next i
            del user_datetimes 
            # Calculate sessions, requests, and durations for each ip
            for dtidx in range(len(user_datetimes_obj)):
                if dtidx != len(user_datetimes_obj):
                    # For each datetime for a user, take difference between next datetime and current. If delta > inactive, 
                    # treat as a new session. Otherwise, add to current session request number and duration
                    tdelt = int(user_datetimes_obj[dtidx+1][0].second) - int(user_datetimes_obj[dtidx][0].second)
                    if tdelt <= inactive:
                        # Take first request of an ip, sub this into sessions after calculating
                        sesh = np.take(session[session[:,0] == i],[0,1,2,3,4,5,6]) 
                        # Replace end date with that of subsequent request (will end on the last request for that session)
                        sesh[3] = user[dtidx+1][1]
                        # Replace end time with that of subsequent request (will end on the last request for that session)
                        sesh[4] = user[dtidx+1][2] 
                        # Add duration subsequent request to session duration
                        sesh[5] = sesh[5] + int((user_datetimes_obj[dtidx+1][0].second))
                        # Add to count of requests for session
                        sesh[6] = sesh[6] + 1
                    else:
                        continue
            # Write the last sesh for an IP to outputfile (sesspath)
            with open(sesspath, 'w', encoding='utf8') as outputfile:
                outputfile.write(','.join(sesh.astype(str)) + '\n')


# Still need to account for same-IP but new session (tdelt > inactive)                        

directory = 'C:/Users/maxca/Documents/GitHub/codingchallenge_edgar-analytics'
sessionization(directory+'/input/log.csv', directory+'/input/inactivity_period.txt', directory+'/output/sessionization.txt')