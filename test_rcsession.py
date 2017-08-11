import argparse
import rcsession


def buildArgParser():
    parser = argparse.ArgumentParser(
        prog='test_rcsession', description='Test rcsession')
    parser.add_argument(
        '--token', help='User auth token',
        required=False)
    return parser.parse_args()


def main():
    # figure out how we should get our token
    # and configure our https session
    if args.token:
        session = rcsession.RCSession(args.token)
    else:
        print("ERROR: No token provided")
        exit(1)
        # session = rcsession.RCSession(rcsession.RCSession.get_token_from_file(self, 'token.json'))
        # session = rcsession.RCSession(rcsession.get_token_from_file(token_file))

    if not session:
        exit(1)

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


args = buildArgParser()

if __name__ == '__main__':
    main()
