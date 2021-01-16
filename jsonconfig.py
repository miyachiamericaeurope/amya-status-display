#!/usr/bin/env python
#python3
import json
#standard python logging
import logging
logger = logging.getLogger(__name__)

class JsonConfig(object):
    def __init__(self, path):
        self._path = path
        try:
            with open(self._path, 'r') as fp:
                self._dict = json.load(fp)
        except Exception as e:
            logger.debug('problem opening json config file..{}'.format(e))
        
    def save(self, path=None):
        if path is None:
            path = self._path
        try:
            with open(path, 'w') as fp:
                json.dump(self._dict, fp, indent=4)
        except Exception as e:
            logger.debug('problem writing json config file..{}'.format(e))
            
    def __str__(self):
        return str(self._dict)
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, item):
        self._dict[key] = item

    def get(self, *keys, default=None):
        if len(keys) == 1:
            if keys[0] not in self._dict:
                return default
            return self._dict[keys[0]]
        else:
            temp = self._dict
            for key in keys[:-1]:
                if key not in temp:
                    return default
                temp = temp[key]
            if keys[-1] not in temp:
                return default
            return temp[keys[-1]]
    
    #def get(self, *args):
    #    if len(args) == 1:
    #        return self._dict[args[0]]
    #    else:
    #        for item in args[1:]:
    #            return self._dict[args[0]].get(item)

    def set(self, newValue, *keys):
        #_keys = keys[:-1]
        temp = self._dict
        for key in keys[:-1]:
            temp  = temp[key]
        temp[keys[-1]] = newValue

    @property
    def json(self):
        return self._dict

    @json.setter
    def json(self, newDict):
        if isinstance(newDict, dict):
            self._dict = newDict

def main():
    config = JsonConfig('mqtt.test-config.json')
    #config = JsonConfig('mqtt.config.json')
    print( config['topics']['error'])
    print(config)
    print(config['credentials']['root_ca'])
    config['credentials']['root_ca']='ca.crt'
    #config.save()
    #config.save('new.config')
    print(config.get('connection','host'))
    print(config.get('publish'))
    keys=['connection', 'host']
    config.set('ubuntu28.local',*keys)
    print(config.get('connection','host'))
    #config.save()
    #config.save('new.config')
    config.set('', *['client', 'client_id'])
    config.save()
    config.json={"totallynew":"dict"}
    print(config.json)
    
    
    
if __name__ == "__main__": 
    import logging
    import logging.handlers
    import sys

    #create local logger
    logger = logging.getLogger(__name__)
    LOG_TO_CONSOLE = True

    if LOG_TO_CONSOLE:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        handler = logging.handlers.RotatingFileHandler(__file__+'.log', maxBytes=5000000, backupCount=1)
    
    formatter = logging.Formatter(fmt='%(asctime)s %(name) -55s %(levelname)-9s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    
    #create a logging whitelist - (comment out code in ~~ block to enable all child loggers)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     loggingWhitelist = ('root', 'plcclient', 'snap7', 'database', '__main__')
#     class Whitelist(logging.Filter):
#         def __init__(self, *whitelist):
#             self.whitelist = [logging.Filter(name) for name in whitelist]
#     
#         def filter(self, record):
#             return any(f.filter(record) for f in self.whitelist)
#     #add the whitelist filter to the handler
#     handler.addFilter(Whitelist(*loggingWhitelist))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #assign the handler to root logger (we use the root logger so that we get output from all child logger used in other modules)
    logging.root.addHandler(handler)
    #set the logging level for root logger
    logging.root.setLevel(logging.DEBUG)

    main()
