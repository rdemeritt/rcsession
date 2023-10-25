from rcsession.rd_utilities import *
import config


def main():
    dff_json = build_dff_config_json()
    config.logger.debug('dff_json: %s ' % dff_json)

    # just list the module config
    if config.args.action == 'LIST':
        print(list_dff_config_for_module(config.session, dff_json).text)

    # submit the document with a actual action
    else:
        print(post_dff_config(config.session, dff_json).text)


def build_dff_config_json():
    dff_dict = {}

    if config.args.module:
        dff_dict['module_name'] = config.args.module

    if config.args.action and config.args.action == 'LIST':
        return dff_dict

    if config.args.action:
        dff_dict['module_status'] = config.args.action

    if config.args.domain_id:
        dff_dict['allowed_domain'] = []
        dff_dict['clear_existing_domains'] = False
        for domain in config.args.domain_id.split(','):
            dff_dict['allowed_domain'].append(domain)

    if config.args.clear_existing:
        dff_dict['clear_existing_domains'] = config.args.clear_existing
    dff_dict = [dff_dict]
    return json.dumps(dff_dict)


def post_dff_config(_session, _dff_json):
    response = _session.post(config.dff_url, data=_dff_json)
    return response


def list_dff_config_for_module(_session, _module_name_dict):
    response = _session.get(config.dff_url, params=_module_name_dict)
    config.logger.debug(response)
    return response


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
    config.RCSession.close_requests(config.session)
