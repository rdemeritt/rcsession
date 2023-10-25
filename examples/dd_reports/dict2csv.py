import config
import csv


def write_dict_to_csv(_src_dict, _dst_csv_file):
        header = _src_dict[0].keys()
        try:
            with open(_dst_csv_file, 'w+', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, header, dialect='excel', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in _src_dict:
                    writer.writerow(row)
            config.logger.info('wrote csv to %s with %s rows and %s columns' %
                               (_dst_csv_file, len(_src_dict), len(header)))
            return True
        except Exception as e:
            config.logger.error('unable to write %s' % _dst_csv_file)
            config.logger.debug(str(e))
            return False
