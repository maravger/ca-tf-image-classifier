#!/usr/bin/python
import json
import csv
import calendar
import datetime
import time

from datetime import datetime


def main():
    f = open('3.cloud_info_48_samples.txt')
    input = json.load(f)
    
    # x="field_score"
    input = map(lambda x: flattenjson( x, "__" ), input)
    columns = [x for row in input for x in row.keys()]

    columns = list([x for x in set(columns) if
        ((x=="duration__value") or (x=="fire_score__value") or
            (x=="size__value"))]) 

    print(input)
    f.close()
    with open ('output.json', 'w') as outfile:
        json.dump(input,outfile)
         
    with open( 'data.csv', 'w' ) as out_file:
        csv_w = csv.writer( out_file )
        csv_w.writerow( columns )

        for i_r in input:
            csv_w.writerow(map(lambda x: i_r.get(x, ""), columns))

    f.close()


def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                if j == "value":
                    if i == "dateCreated":
                        val[i + delim + j] = UTC_time_to_epoch(get[j])
                    else:    
                        val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def UTC_time_to_epoch(timestamp):
    p = '%Y-%m-%dT%H:%M:%S.%fZ'
    timestamp = datetime.strptime(timestamp, p)
    then = timestamp
    epoch = time.mktime(then.timetuple()) + then.microsecond/1e6
    #print (epoch)
    return epoch 


if __name__ == "__main__":
        main()
