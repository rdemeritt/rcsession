import argparse
import rcsession
import os
from urllib.parse import quote_plus
import json


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='test_rcsession', description='Test rcsession')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('--token', help='User auth via Red Cloak Token')
    auth_group.add_argument('--key', help='User auth via API key')
    return parser.parse_args()


def dump_url_response(_session, _url):
        print(_url)
        return _session.session.get(_url).text


def main():
    # figure out how we should get our token
    # and configure our https session
    if args.token:
        redcloak_session = rcsession.RCSession(_token=args.token)

    elif args.key:
        redcloak_session = rcsession.RCSession(_key=args.key)

    else:
        print("ERROR: No token provided")
        exit(1)

    if not redcloak_session:
        exit(1)

    # limit results
    count = '?count=%s'

    # dump some pages
    print("TOKEN:\n" + str(redcloak_session.get_token()))
    print("\nFRIENDLY NAME:\n" + str(redcloak_session.user_friendly_name))
    print("\nAETD DOMAIN:\n" +
          redcloak_session.session.get(redcloak_session.index_url, params={'domain': 'd32c7944'}).text)
    print("\nCLIENT DOMAINS:\n" +
          redcloak_session.session.get(redcloak_session.client_domains_url, params={'count': '1'}).text)
    print("\nWATCHLISTS:\n" +
          redcloak_session.session.get(redcloak_session.watchlists_url, params={'count': '1'}).text)
    print("\nHOSTS:\n" +
          redcloak_session.session.get(redcloak_session.hosts_url, params={'count': '1'}).text)

    # print the RCSession info
    print("\nRCSESSION INFO:\n" + str(redcloak_session.__dict__))

    # print out the requests session info
    print("\nREQUESTS INFO:\n" + str(redcloak_session.__dict__['session'].__dict__))

    # close_requests our https session
    print("Closing %s: " % redcloak_session.__dict__['session'])
    redcloak_session.close_requests()
    print("Closed")

    exit(0)


args = build_arg_parser()

if __name__ == '__main__':
    main()
