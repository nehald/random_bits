import csv
import pygeoip
import datetime

gi = pygeoip.GeoIP('/opt/GeoLiteCity.dat', pygeoip.MMAP_CACHE)


def time_convert(t):
    try:
        hours, mins, secs = t.split(":")
        whole_secs, micro_sec = secs.split(".")
        dt = (datetime.timedelta(hours=int(hours), minutes=int(
            min), seconds=int(whole_secs), microseconds=int(micro_sec)))
    	return dt
    except:
        pass

with open("/home/nehal/OLD/footest.csv", "rb") as csvfile:
    COMMA = ","
    rd = csv.reader(csvfile, delimiter=',')
    fields = rd.next()
    for row in rd:
        f = dict(zip(fields, row))
        try:
            src_geo = gi.record_by_addr(f['src_ip'])
            dest_geo = gi.record_by_addr(f['dest_ip'])
            if src_geo != dest_geo:
                src_city = src_geo['city']
                src_region = src_geo['region_name']
                src_country = src_geo['country_code']
                src = src_city + " " + \
                    src_region + " " + src_country

                dest_city = dest_geo['city']
                dest_region = dest_geo['region_name']
                dest_country = dest_geo[
                    'country_code']
                dest = dest_city + " " + \
                    dest_region + \
                    " " + dest_country
                arrow = src + "---->" + dest
                start_time = (
                    datetime.datetime.now() + time_convert(f['time']))
                end_time = start_time + \
                    time_convert(f['conn_length'])
                outstring = arrow + COMMA + start_time.isoformat() + COMMA + end_time.isoformat()\
			+COMMA + str(src_geo['latitude']) + COMMA + str(src_geo['longitude'])\
                    	+COMMA + str(dest_geo['latitude']) + COMMA + str(dest_geo['longitude'])
		print outstring
        except:
            pass
