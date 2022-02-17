#!/usr/bin/env python3
import csv
import operator
import re
user = {}
error = {}
with open('syslog.log', 'r') as s:
    pattern1 = r'ERROR ([\w\' ]*).*\((.*)\)'
    pattern2 = r'INFO ([\w ]*).*\((.*)\)'
    for line in s:
        if 'ERROR' in line:
            err = re.search(pattern1, line).group(1).strip()
            usr = re.search(pattern1, line).group(2)
            error[err] = error.get(err, 0) + 1
            if usr not in user.keys():
                user[usr] = [0, 1]
            else:
                user[usr][1] += 1
        if 'INFO' in line:
            inf = re.search(pattern2, line)
            usr = re.search(pattern2, line).group(2)
            if usr not in user.keys():
                user[usr] = [1,0]
            else:
                user[usr][0] += 1
errors = sorted(error.items(), key = operator.itemgetter(1), reverse = True)
users = sorted(user.items(), key = operator.itemgetter(0))
errors = [('Error', 'Count')] + errors
users2 = [['Username', 'INFO', 'ERROR']] + [[list(u)[0], list(u)[1][0], list(u)[1][1]] for u in users]
with open('error_message.csv', 'w') as e:
    writer = csv.writer(e)
    writer.writerows(errors)
with open('user_statistics.csv', 'w') as u:
    writer = csv.writer(u)
    writer.writerows(users2)