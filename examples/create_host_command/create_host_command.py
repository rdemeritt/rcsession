from rcsession.rd_utilities import *
import config


def get_host_command_id(_session):
    config.logger.info('getting new host command ID')
    response = _session.post(_session.host_commands_url, params={'create': 'true'})

    if response.status_code is not 201:
        config.logger.error('unable to get unique host command ID')
        return False

    config.logger.debug(response.headers)
    config.logger.debug(response.headers['location'])

    hc_id = response.headers['location'].split(',')[1].split('/')[2].split('?')[0]

    config.logger.info('the host command ID is: %s' % hc_id)

    return hc_id


def build_enable_lacuna_host_command_json(_domain_id, _name):
    en_lacuna_json = [
        {
            "id": None,
            "name": _name,
            "minimum_version": 0,
            "maximum_version": 0,
            "enabled": False,
            "tag": [],
            "domain_id": _domain_id,
            "f_response_enabled": False,
            "destroy_agent_enabled": False,
            "config_update": [
                {
                    "path": "modules.lacuna.enabled",
                    "value": {
                        "boolean": True
                    }
                }
            ],
            "global_config_update": [],
            "log_requests": [],
            "host_ids": []
        }
    ]

    en_lacuna_json[0]['id'] = get_host_command_id(config.session)

    if config.args.enable is True:
        pass
    else:
        en_lacuna_json[0]['enabled'] = False

    return en_lacuna_json[0]


def build_disable_inspector_host_command_json(_domain_id, _name):
    dis_inspector_json = [
        {
            "id": None,
            "name": _name,
            "minimum_version": 0,
            "maximum_version": 0,
            "enabled": False,
            "tag": [],
            "domain_id": _domain_id,
            "f_response_enabled": False,
            "destroy_agent_enabled": False,
            "config_update": [
                {
                    "path": "modules.inspector.enabled",
                    "value": {
                        "boolean": False
                    }
                }
            ],
            "global_config_update": [],
            "log_requests": [],
            "host_ids": []
        }
    ]

    dis_inspector_json[0]['id'] = get_host_command_id(config.session)

    if config.args.enable is True:
        pass
    else:
        dis_inspector_json[0]['enabled'] = False

    return dis_inspector_json[0]


def build_global_host_command_json(_domain_id):
    hc_json = [
        {
            "id": None,
            "host_ids": [],
            "config_update": [],
            "global_config_update": [
                {
                    "path": "modules.fcm.enabled",
                    "value": {
                        "boolean": False
                    }
                }
            ],
            "log_requests": [],
            "name": None,
            "domain_id": _domain_id,
            "tag": ['disable FCM'],
            "enabled": True,
            "minimum_version": 0,
            "maximum_version": 0,
            "destroy_agent_enabled": False,
            "f_response_enabled": False
        }
    ]

    hc_json[0]['id'] = get_host_command_id(config.session)
    hc_json[0]['name'] = 'disable FCM global'

    if config.args.enable is True:
        pass
    else:
        hc_json[0]['enabled'] = False

    return hc_json[0]


def populate_domain_id(_hc_json):
    for domain_id in config.args.domain_id.split(','):
        config.logger.debug('adding %s to domain_id' % domain_id)
        _hc_json['domain_id'] = domain_id

    config.logger.debug(_hc_json)
    return _hc_json


def populate_host_id(_hc_json, _hosts_json):
    hosts_json = get_json_file_contents(_hosts_json)
    host_ids= []

    for host in hosts_json['hosts']:
        host_ids.append(host['id'])
    config.logger.debug('host_ids: ' + str(host_ids))

    _hc_json['host_ids'] = host_ids
    config.logger.debug(_hc_json)
    return _hc_json


def main():
    dis_insp_json = populate_host_id(
        build_disable_inspector_host_command_json(config.args.domain_id, 'disable inspector - all virt hosts'), 'virt_hosts.json')
    # en_lacuna_hc_json = populate_host_id(
    #     build_enable_lacuna_host_command_json(config.args.domain_id, 'test again'), 'host_list.json')
    response = config.session.put(config.session.host_commands_url + '/' + dis_insp_json['id'], json=dis_insp_json)
    config.logger.debug(response.text)


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
