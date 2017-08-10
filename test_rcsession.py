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
        session = rcsession.setup_session(args.token)
    else:
        session = rcsession.setup_session(rcsession.get_token_from_file(token_file))

    if not session:
        exit(1)

    print(rcsession.get_token(session))
    rcsession.renew_token(session, "2017-09-30")
    print(rcsession.get_token(session))

    exit(0)


args = buildArgParser()

if __name__ == '__main__':
    main()
