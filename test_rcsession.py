import argparse
import rcsession


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='test_rcsession', description='Test rcsession')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('--token', help='User auth via Red Cloak Token')
    auth_group.add_argument('--key', help='User auth via API key')
    return parser.parse_args()


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
        # session = rcsession.RCSession(rcsession.RCSession.get_token_from_file(self, 'token.json'))
        # session = rcsession.RCSession(rcsession.get_token_from_file(token_file))

    if not session:
        exit(1)

    if args.token:
        print(session.get_token())
        print(session.user_friendly_name)
        print(session.renew_token())
        print(session.get_token())
        print(session.user_friendly_name)
        print(session.is_token_valid())

    # print the RCSession info
    print("\n" + str(session.__dict__))

    # print out the requests session info
    print("\n" + str(session.__dict__['session'].__dict__))

    # close_requests our https session
    print("Closing %s: " % session.__dict__['session'])
    session.close_requests()
    print("Closed")

    exit(0)


args = build_arg_parser()

if __name__ == '__main__':
    main()
