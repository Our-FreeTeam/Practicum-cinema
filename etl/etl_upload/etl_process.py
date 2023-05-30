import logging
from time import sleep

from storage_config import settings


class EtlProcess:
    def __init__(self, index_name, pg_extractor, es_uploader):
        logging.basicConfig(format=settings.log_format, level=settings.log_level)

        self.pg_extractor = pg_extractor
        self.es_uploader = es_uploader

        last_modified, try_count = self.es_uploader.get_last_modified()
        data = self.pg_extractor.get_data(last_modified)
        logging.info('Index "%s" have %d item(s) for transfer' % (index_name, len(data)))

        if data:
            new_last_modified, new_try_count = self.get_new_try_count(data, last_modified, try_count)
            if (new_try_count < settings.max_modified_retries_count or last_modified != new_last_modified):
                is_errors = self.es_uploader.upload_data(data)
                if is_errors:
                    logging.error("Can't load data in index '%s'!" % index_name)
                else:
                    self.es_uploader.set_last_modified(new_last_modified, new_try_count)
            else:
                self.delay(settings.load_delay)
        else:
            self.delay(settings.load_delay)

    @staticmethod
    def get_new_try_count(data, last_modified, try_count):
        new_last_modified = data[-1].modified
        if last_modified == new_last_modified:
            try_count += 1
        else:
            try_count = 0
        return new_last_modified, try_count

    @staticmethod
    def delay(delay_time: float):
        logging.warning('Upload delay: %s s', delay_time)
        with open('./ETL_FINISHED.flag', 'w') as f:
            f.write('Create a new text file!')
        sleep(delay_time)
