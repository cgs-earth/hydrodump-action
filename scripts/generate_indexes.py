"""
Print CREATE INDEX statements for every pygeoapi feature provider's id_field.

Usage: python3 generate_indexes.py path/to/pygeoapi.config.yml > indexes.sql

yaml.safe_load resolves `<<: *provider_defaults` merge keys, so providers
that only inherit `id_field` from an anchor are included. Tile providers are
skipped, and (table, id_field) pairs are deduplicated.
"""
import re
import sys

import yaml

IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def main(path):
    with open(path) as fh:
        config = yaml.safe_load(fh)

    seen = set()
    for name, resource in config['resources'].items():
        for provider in resource.get('providers', []):
            if provider.get('type') != 'feature' or 'table' not in provider:
                continue
            if 'id_field' not in provider:
                sys.exit(f'resource {name}: feature provider has no id_field')
            key = (provider['table'], provider['id_field'])
            for ident in key:
                if not IDENTIFIER.match(str(ident)):
                    sys.exit(f'resource {name}: unsafe identifier {ident!r}')
            if key in seen:
                continue
            seen.add(key)
            table, id_field = key
            print(f'CREATE INDEX IF NOT EXISTS {table}_{id_field}_idx '
                  f'ON public.{table} ({id_field});')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
