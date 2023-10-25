
from rcsession.rd_utilities import *
import config


def main():
    if config.args.wl_id:
        get_response = config.session.get(config.session.watchlists_url + '/' + config.args.wl_id)
        wl_json = json.loads(get_response.text)
        new_subscribers = []
        config.logger.debug(wl_json['subscriber'])
        if config.args.delete:
            for subscriber in wl_json['subscriber']:
                if subscriber['email'] == config.args.email and subscriber['allowed_domain'][0] == config.args.domain_id:
                    config.logger.info(
                        'removing email: %s and allowed_domain: %s' % (subscriber['email'], subscriber['allowed_domain']))
                    pass
                else:
                    new_subscribers.append(subscriber)
            wl_json['subscriber'] = new_subscribers
            put_response = config.session.put(config.session.watchlists_url + '/' + config.args.wl_id, json=wl_json)
            config.logger.debug("new: %s" % new_subscribers)
            config.logger.debug(config.session.get(config.session.watchlists_url + '/' + config.args.wl_id).text)

        if config.args.add:
            wl_json['subscriber'].append(
                {'allowed_domain': ['%s' % config.args.domain_id],
                 'email': '%s' % config.args.email}
            )
            put_response = config.session.put(config.session.watchlists_url + '/' + config.args.wl_id, json=wl_json)
            config.logger.debug(config.session.get(config.session.watchlists_url + '/' + config.args.wl_id).text)


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
