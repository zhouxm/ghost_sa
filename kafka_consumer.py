# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys

sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.api import insert_data, insert_installation_track, insert_shortcut_history, insert_shortcut_read
import json
from component.kafka_op import get_message_from_kafka
import traceback
# import multiprocessing
from configs.export import write_to_log
from concurrent.futures import ThreadPoolExecutor


def use_kafka():
    results = get_message_from_kafka()
    with ThreadPoolExecutor(max_workers=8) as worker:
        for result in results:
            worker.submit(do_insert, result)


def do_insert(msg):
    try:
        group = json.loads(msg.value.decode('utf-8'))['group'] if "group" in json.loads(msg.value.decode('utf-8')) else None
        data = json.loads(msg.value.decode('utf-8'))['data']
        offset = msg.offset
        print(offset)
        if group == 'event_track':
            # print(data['project'])
            insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'],
                        Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'],
                        Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                        ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'],
                        ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'],
                        ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
        elif group == 'installation_track':
            insert_installation_track(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'],
                                      Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'],
                                      Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                                      ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'],
                                      ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'],
                                      ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'],
                                      updated_at=data['updated_at'], use_kafka=False)
        elif group == 'shortcut_history':
            insert_shortcut_history(short_url=data['short_url'], result=data['status'], cost_time=data['time2'], ip=data['ip'], user_agent=data['user_agent'],
                                    accept_language=data['accept_language'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'],
                                    ua_version=data['ua_version'], ua_language=data['ua_language'], created_at=data['created_at'])
        elif group == 'shortcut_read':
            insert_shortcut_read(short_url=data['short_url'], ip=data['ip'], user_agent=data['user_agent'], accept_language=data['accept_language'],
                                 ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'],
                                 referrer=data['referrer'], created_at=data['created_at'])
        else:
            insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'],
                        Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'],
                        Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                        ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'],
                        ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'],
                        ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='kafka_consumer',
                     defname='do_insert', result=error)


if __name__ == "__main__":
    use_kafka()
