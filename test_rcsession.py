import argparse
import rcsession
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
        session = rcsession.RCSession(_token=args.token)

    elif args.key:
        session = rcsession.RCSession(_key=args.key)

    else:
        print("ERROR: No token provided")
        exit(1)

    if not session:
        exit(1)

    if args.key:
        pass

    if args.token:
        pass

    # limit results
    count = '?count=%s' % '5'

    # dump some pages
    print("TOKEN:\n" + str(session.get_token()))
    print("\nFRIENDLY NAME:\n" + str(session.user_friendly_name))
    print("\nCLIENT DOMAINS:\n" + str(
        dump_url_response(session, session.client_domains_url + count)))
    print("\nWATCHLISTS:\n" + str(
        dump_url_response(session, session.watchlists_url + count)))
    print("\nHOSTS:\n" + str(
        dump_url_response(session, session.hosts_url + count)))

    # print the RCSession info
    print("\nRCSESSION INFO:\n" + str(session.__dict__))

    # print out the requests session info
    print("\nREQUESTS INFO:\n" + str(session.__dict__['session'].__dict__))

    # close_requests our https session
    print("Closing %s: " % session.__dict__['session'])
    session.close_requests()
    print("Closed")

    exit(0)


args = build_arg_parser()

if __name__ == '__main__':
    main()
