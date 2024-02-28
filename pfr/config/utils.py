import yaml
from jsonschema import validate, ValidationError
from logging import getLogger
from copy import copy
import re
import os

LOG = getLogger(__name__)


def _camel_case_to_underscored(text):
    return re.sub(r'([A-Z])', r'_\1', text).lower()


CONFIG_SCHEMA_FILE = 'config.schema.yaml'

def load_config(cmd_args):
    with open(os.path.join(os.path.dirname(__file__), CONFIG_SCHEMA_FILE), 'r') as f_schema:
        cfg_schema = yaml.safe_load(f_schema)
        with open(cmd_args.config, 'r') as f_config:
            config = yaml.safe_load(f_config)
            try:
                validate(instance=config, schema=cfg_schema)
            except ValidationError:
                print("""The configuration file seems to be incorrect. Please make sure that it satisfies the following constraints:
                
                input:
                  timestampMask: "%Y-%m-%dT%H:%M:%S"    #timestamp mask used for start/end of the activity (required)
                  processName: process                  #process name defined by user (required)
                  eventlogInputColumns:                 #mapping of eventlog columns             
                    caseId: case_id                     #requiredobligator
                    activity: activity                  #required
                    endTimestamp: end_time              #required/optional
                    startTimestamp: start_time          #required/optional
                    resource: resource                  #optional""")
                exit(1)
    params = copy(cmd_args)
    for key, p_value in config.get('params', {}).items():
        p = _camel_case_to_underscored(key)
        if p not in cmd_args:
            LOG.warn("Ignoring unrecognized config param: '%s'", key)
        elif cmd_args.__getattribute__(p):
            LOG.warn("Ignoring config param '%s', using command line value: %s", key, cmd_args.__getattribute__(p))
        else:
            params.__setattr__(p, p_value)
    return config, params
