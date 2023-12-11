import yaml
from jsonschema import validate
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
            validate(instance=config, schema=cfg_schema)
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
