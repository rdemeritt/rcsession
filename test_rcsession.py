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
        session = rcsession.RCSession(RCSession.get_token_from_file('token.json'))
        # session = rcsession.RCSession(rcsession.get_token_from_file(token_file))

    if not session:
        exit(1)

    print(session.get_token())
    print(session.username)
    print(session.renew_token())
    print(session.get_token())
    print(session.username)
    exit(0)


args = buildArgParser()

if __name__ == '__main__':
    main()
