import config
import dd_reports
import json
from dict2csv import write_dict_to_csv


def populate_host_contact_dict(_dict):
    populated = []
    for host in _dict:
        ooc_dict = dict()
        ooc_dict['hostname'] = host['name']
        ooc_dict['type'] = host['system_information']['product_type']
        ooc_dict['version'] = host['system_information']['version']
        ooc_dict['last_connect_time'] = host['last_connect_time']
        ooc_dict['ip_addresses'] = host['system_information']['ip_address']
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


def populate_fcm_report_dict(_dict):
    populated_dict = []
    for event in _dict:
        try:
            event_dict = dict()
            event_dict['date'] = event['event_time']
            event_dict['hostname'] = dd_reports.hostnamebyhostid(config.session, event['id']['host_id'])
            event_dict['event_color'] = event['color']
            event_dict['watch_name'] = dd_reports.watchnamebywatchid(config.session, event['watch_id'])
            event_dict['change_type'] = event['location_metadata']['entry_metadata'][0]['change_type']
            event_dict['entry_type'] = event['location_metadata']['entry_metadata'][0]['entry_type']
            if 'relative_name' in event['location_metadata']['entry_metadata'][0]:
                event_dict['full_path'] = event['location_metadata']['location']['absolute_path'] + '\\' + \
                                            event['location_metadata']['entry_metadata'][0]['relative_name']
            else:
                event_dict['full_path'] = event['location_metadata']['location']['absolute_path']
            if 'metadata' in event['location_metadata']['entry_metadata'][0] and \
                    'permission_attributes' in event['location_metadata']['entry_metadata'][0]['metadata']:
                event_dict['attributes'] = event['location_metadata']['entry_metadata'][0]['metadata']['permission_attributes']
            else:
                event_dict['attributes'] = 'null'

            populated_dict.append(event_dict)
        except Exception as e:
            config.logger.debug(str(e) + ': %s' % event)
            return False
    return populated_dict


def get_fcm_events(_session, _s_dict, _bulk=True):
    fcm_filter = {
        'domain': '%s' % config.args.domain,
        'filter': 'event_time: [%s TO %s]' % (_s_dict['qt_start'], _s_dict['qt_end']),
        'bulk': '%s' % _bulk,
        'name': 'get_fcm_events_%s' % config.start_time
    }

    config.logger.debug('fcm_filter: %s' % fcm_filter)
    fcm_response = _session.get(_session.fcm_events_url, params=fcm_filter)

    if fcm_response.status_code is not 200:
        return False
    if _bulk is False:
        return json.loads(fcm_response.text)
    else:
        deferred_job = json.loads(fcm_response.text)
        config.logger.debug('deferred job_id: %s' % deferred_job['uuid'])
        deferred_job_results_json = config.session.fetch_deferred_job(deferred_job['uuid'])
        return deferred_job_results_json


def generate_events_report():
    fcm_dates_dict = {
        'qt_start': '{}',
        'qt_end': '{}'
    }

    # format our search strings for the range
    fcm_dates_dict['qt_start'] = fcm_dates_dict['qt_start'].format(config.args.start)
    fcm_dates_dict['qt_end'] = fcm_dates_dict['qt_end'].format(config.args.end)

    # search for the fcm events using dates
    search_results_json = get_fcm_events(config.session, fcm_dates_dict)

    # once we get the results, let's build out our csv
    formatted_dict = populate_fcm_report_dict(search_results_json['fcm_change_events'])
    write_dict_to_csv(formatted_dict, config.args.output)
    return True
