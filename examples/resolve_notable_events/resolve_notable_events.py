"""
Created by Ron DeMeritt <rdemeritt@gmail.com>

"""
import argparse
import json
from rcsession import rcsession
from rcsession.rd_utilities import *
from log import build_logger


def get_notable_hosts(_session, _color, _count=10000):
    hosts_filter = {
        "color": "%s" % _color,
        "count": _count
    }
    response = _session.get(_session.hosts_url, params=hosts_filter)
    response_json = json.loads(response.text)
    # print("Number of hosts: %s" % len(response_json['hosts']))
    return response_json


def get_notable_events_from_host(_session, _host_id, _count=10000):
    hcc_filter = {
        "host_id": "%s" % _host_id,
        "count": _count
    }
    # response = _session.get(_session.hcc_url, params=hcc_filter)
    # response_json = json.loads(response.text)
    notable_events_json = json.loads(_session.session.get(_session.hcc_url, params=hcc_filter).text)
    return notable_events_json


def resolve_notable_event(_session, _event_type, _event_url, _status, _comment):

    response = _session.session.get(_session.base_url + _event_url)
    if response.status_code != 200:
        # print("Bad Event: ", _event_type, _event_url)
        return False

    notable_event_json = json.loads(response.text)
    # notable_event_json = json.loads(_session.get(rc_url + _event_url).text)

    host_id = notable_event_json["id"]["host_id"]
    resolved_by = _session.user_friendly_name
    # print(
    #     "Processing %s by %s as status %s with comment \"%s\""
    #     % (_event_url, user_name, _status, _comment))

    if _event_type == 'watchlist_result':
        # fetch instance_id
        instance_id = notable_event_json["id"]["instance_id"]

        resolve_watchlist_result(
            _session, host_id, instance_id,
            _event_type, resolved_by, _status, _comment)

    elif _event_type == 'persistence_event':
        resolve_persistence_event(
            _session, notable_event_json["id"]["event_id"], host_id,
            _event_type, resolved_by, _status, _comment)

    elif _event_type == 'process':
        resolve_process(
            _session, host_id, notable_event_json["id"]["pid"],
            notable_event_json["id"]["time_window"],
            _event_type, resolved_by, _status, _comment)

    elif _event_type == 'artifact':
        resolve_rule_result(
            _session, host_id, notable_event_json["id"]["instance_id"],
            'ruleresult', resolved_by, _status, _comment)
    return True


def resolve_process(
    _session, _host_id, _pid, _time_window,
    _event_type, _resolved_by, _status, _comment
):
    rp_dict = {
        "id": {
            "host_id": "%s" % _host_id,
            "pid": _pid,
            "time_window": _time_window
        },
        "type": "%s" % _event_type,
        "resolved_by": "%s" % _resolved_by,
        "status": _status,
        "comment": "%s" % _comment
    }

    response = _session.session.post(_session.event_resolution_url, json=rp_dict)

    if response.status_code != 200:
        print(
            'Recieved status code:', response.status_code,
            'for: ', rp_dict)
        return False
    print('Resolved: ', rp_dict)
    return True


def resolve_watchlist_result(
    _session, _host_id, _instance_id, _event_type,
    _resolved_by, _status, _comment
):
    rwlr_dict = {
        "id": {
            "host_id": "%s" % _host_id,
            "instance_id": "%s" % _instance_id
        },
        "type": "%s" % _event_type,
        "resolved_by": "%s" % _resolved_by,
        "status": _status,
        "comment": "%s" % _comment
    }

    response = _session.post(_session.event_resolution_url, json=rwlr_dict)

    if response.status_code != 200:
        print(
            'ERROR: Recieved status code: ', response.status_code,
            'for: ', rwlr_dict)
        return False
    print('Resolved: ', rwlr_dict)
    return True


def resolve_persistence_event(
        _session, _event_id, _host_id, _event_type,
        _resolved_by, _status, _comment
):

    rpe_dict = {
        "id": {
            "event_id": "%s" % _event_id,
            "host_id": "%s" % _host_id
        },
        "type": "%s" % _event_type,
        "resolved_by": "%s" % _resolved_by,
        "status": _status,
        "comment": "%s" % _comment
    }

    response = _session.session.post(_session.event_resolution_url, json=rpe_dict)

    if response.status_code != 200:
        print(
            'ERROR: Recieved status code: ', response.status_code,
            'for: ', rpe_dict)
        return False
    print('Resolved: ', rpe_dict)
    return True


def resolve_rule_result(
        _session, _host_id, _instance_id, _event_type,
        _resolved_by, _status, _comment
):
    rrr_dict = {
        "id": {
            "host_id": "%s" % _host_id,
            "instance_id": "%s" % _instance_id
        },
        "type": "%s" % _event_type,
        "resolved_by": "%s" % _resolved_by,
        "status": _status,
        "comment": "%s" % _comment
    }

    response = _session.session.post(_session.event_resolution_url, json=rrr_dict)

    if response.status_code != 200:
        print(
            'ERROR: Recieved status code: ', response.status_code,
            'for: ', rrr_dict)
        return False
    print('Resolved: ', rrr_dict)
    return True


def delete_color_contributions(_session, _notable_event):
    response = _session.delete(
        _session.hcc_url + "/" + _notable_event['id']['host_id'] + ":" + _notable_event['id']['object_hash_id'])
    if response.status_code not in (200, 204):
        return False
    if args.verbose:
        print("Deleted Color Contribution: ", _notable_event)

    return True


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='resolve_notable_events', description='Resolve Notable Events')
    parser.add_argument(
        '--host_id', help='host_id of endpoint to resolve',
        required=False)
    # parser.add_argument(
    #     '--notable_events', help='URL of Notable Event(s) to resolve',
    #     required=False)
    parser.add_argument(
        '--status', choices=range(0, 6), type=int,
        required=True, help='Resolve code for Notable Events')
    parser.add_argument(
        '--comment', help='Comment for Notable Events',
        required=True)
    parser.add_argument(
        '--count', help='Resolve N number of Notable Events', type=int,
        required=False)
    parser.add_argument(
        '--nefile', type=open,
        required=False, help='File containing Notable Events to resolve')
    parser.add_argument(
        '--force', required=False, help='Force the deletion of event if clean resolution fails.',
        action='store_true')
    parser.add_argument(
        '--delete', required=False,
        help='Delete the Color Contributions instead of resolving them.  This is destructive use with caution.',
        action='store_true')
    parser.add_argument(
        '--verbose', required=False, help='Print a bit more information', action='store_true')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        '--token', help='User auth via Red Cloak Token')
    auth_group.add_argument(
        '--key', help='User auth via API key')
    return parser.parse_args()


output_file = 'output.json'
json_output = []


def main():
    # figure out how we should get our token and configure our https session
    if args.token:
        session = rcsession.RCSession(_token=args.token)

    elif args.key:
        session = rcsession.RCSession(_key=args.key)

    # drop out if we don't have a way to setup session
    else:
        logger.error('No token or key provided')
        exit(1)

    # check to see if our session was successfully created
    if not session:
        exit(2)

    # figure out how we should get our notable events
    if args.nefile:
        print('Getting Notable Events from file %s' % args.nefile.name)
        notable_events = get_json_file_contents(args.nefile.name)
    elif args.host_id:
        print("Resolving Notable Events for host_id: %s" % args.host_id)
        if args.count:
            notable_events = get_notable_events_from_host(session, args.host_id, args.count)
        else:
            notable_events = get_notable_events_from_host(session, args.host_id)
    else:
        print('I need a way to know which events i should resolve...')
        exit(1)

    print('Saved list of events to resolve in %s' % output_file)
    write_json(notable_events, output_file)

    # for notable_event in notable_events["watchlist_results"]:
    #     # print(notable_event)
    #     resolve_watchlist_result(
    #         session, notable_event["id"]["host_id"],notable_event["id"]["instance_id"],
    #         "watchlist_result", user_name, args.status, args.comment)

    for notable_event in notable_events["host_color_contributions"]:
        # print(notable_event)
        if args.delete:
            if not delete_color_contributions(session, notable_event):
                print("Error: unable to delete event")
        elif not resolve_notable_event(
                session, notable_event["event_type"],
                notable_event["event_url"].strip("/"), args.status, args.comment):
            if args.force:
                print("Warn: unable to resolve event... forcing:", notable_event)
                if not delete_color_contributions(session, notable_event):
                    print("Error: unable to delete event")
            else:
                print("Warn: unable to resolve event... skipping:", notable_event)
    session.session.close()


args = build_arg_parser()
logger = build_logger()

# kick off the whole thing
if __name__ == '__main__':
    logger.info('Starting')
    main()
