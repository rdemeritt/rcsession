import config
import host_reports_example
import json
from dict2csv import write_dict_to_csv


def populate_host_contact_dict(_dict):
    populated = []
    for host in _dict:
        config.logger.debug(host)
        ooc_dict = dict()
        ooc_dict['hostname'] = host['name']
        # ooc_dict['type'] = host['system_information']['product_type']
        # ooc_dict['version'] = host['system_information']['version']
        ooc_dict['last_connect_time'] = host['last_connect_time']
        if 'system_information' in host and 'ip_address' in host['system_information']:
            ooc_dict['ip_addresses'] = host['system_information']['ip_address']
        else:
            ooc_dict['ip_addresses'] = 'missing'
        populated.append(ooc_dict)
    return populated


def get_ooc_hosts(_session, _bulk=True):
    ooc_hosts = []
    for state in ('inactive', 'lost'):
        hosts_out_of_contact_search = {
            'domain': '%s' % config.args.domain,
            'health_state': '%s' % state,
            'bulk': '%s' % _bulk,
            'name': '%s_ooc_search_%s' % (state, config.start_time)
        }
        ooc_response = _session.get(config.session.hosts_url, params=hosts_out_of_contact_search)
        if ooc_response.status_code is not 200:
            config.logger.warn('did not get 200, got %s instead... skipping %s hosts' % (ooc_response.status_code, state))
            break
        else:
            deferred_job = json.loads(ooc_response.text)
            config.logger.debug('deferred job_id: %s' % deferred_job['uuid'])
            deferred_job_results_json = config.session.fetch_deferred_job(deferred_job['uuid'])
            for host in deferred_job_results_json['hosts']:
                ooc_hosts.append(host)
    return ooc_hosts


def generate_ooc_report():
    search_results_json = get_ooc_hosts(config.session)
    formatted_dict = populate_host_contact_dict(search_results_json)
    write_dict_to_csv(formatted_dict, config.args.output)
    return True


def get_ic_hosts(_session, _bulk=True):
    hosts_in_contact_search = {
        'domain': '%s' % config.args.domain,
        'health_state': 'healthy',
        'bulk': '%s' % _bulk,
        'name': 'ic_search_%s' % config.start_time
    }

    ic_response = _session.get(config.session.hosts_url, params=hosts_in_contact_search)
    if ic_response.status_code is not 200:
        config.logger.warn('did not get 200, got %s instead' % ic_response.status_code)
        return False
    else:
        deferred_job = json.loads(ic_response.text)
        config.logger.debug('deferred job_id: %s' % deferred_job['uuid'])
        deferred_job_results_json = config.session.fetch_deferred_job(deferred_job['uuid'])
    return deferred_job_results_json['hosts']


def generate_ic_report():
    search_results_json = get_ic_hosts(config.session)
    formatted_dict = populate_host_contact_dict(search_results_json)
    write_dict_to_csv(formatted_dict, config.args.output)
    return True
