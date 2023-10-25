import config


def main():
    if config.args.host_id_list:
        # open up host_id file and read all lines
        with open(config.args.host_id_list) as file:
            host_list = file.readlines()
            file.close()
            config.logger.debug(host_list)

        for host_id in host_list:
            host_id = host_id.rstrip()
            action = 0
            if config.args.action == 'isolate':
                action = 1
            elif config.args.action == 'integrate':
                action = 2

            isolate_cmd = dict(host_id=host_id, reason=config.args.reason, action=action)
            config.logger.debug('isolate_cmd: %s' % isolate_cmd)
            response = config.session.post(config.session.isolate_url, json=isolate_cmd)
            config.logger.debug(response.status_code)

            if response.status_code != 200:
                config.logger.warning('Host %s was not %sd' % (host_id, config.args.action))
            else:
                config.logger.info('Host %s was %sd' % (host_id, config.args.action))

    # close our http session
    config.session.close_requests()


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
