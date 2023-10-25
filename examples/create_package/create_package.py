"""
Created by Ron DeMeritt <rdemeritt@gmail.com>

"""
import argparse
from rcsession import rcsession, rd_utilities


def create_package(_session, _package_json):
    response = _session.session.post(_session.packages_url, json=_package_json)

    if args.verbose:
        print(
            'Recieved status code:', response.status_code,
            'for: ', _package_json)

    if response.status_code not in (200, 201):
        return False
    return True


def build_arg_parser():
    parser = argparse.ArgumentParser(prog='create_package', description='Create a package')
    parser.add_argument('--key', help='User auth key', required=True)
    parser.add_argument('--package_file', type=open, required=True, help='File containing JSON package definition')
    parser.add_argument('--verbose', required=False, help='Print a bit more information', action='store_true')
    return parser.parse_args()


output_file = 'output.json'
json_output = []

args = build_arg_parser()

# figure out how we should get our key
# and configure our https session
if args.key:
    session = rcsession.RCSession(_key=args.key)
if not session:
    exit(1)

# get our package definition file
if args.package_file:
    print('Getting package definition from file %s' % args.package_file.name)
    package_definition = rd_utilities.get_json_file_contents(args.package_file.name)
else:
    print('I need a way to know what kind of a package you want...')
    exit(1)

print('Saved package definition in %s' % output_file)
rd_utilities.write_json(package_definition, output_file)

create_package(session, package_definition)
session.session.close()
