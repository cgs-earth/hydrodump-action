# hydrodump-action
Create a Postgis SQL dump from a Hydroshare resource

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `username` | `ChangeMe` | Hydroshare username |
| `password` | `ChangeMe` | Hydroshare password |
| `resource` | `3295a17b4cc24d34bd6a5c5aaf753c50` | Hydroshare resource id |
| `db` | `reference` | Postgres database name (the dump is written to `<db>.sql.gz`) |
| `dbuser` | `root` | Database user |
| `dbpass` | `ChangeMe` | Database password |
| `pygeoapi-config` | `''` | Optional path, in the calling repo, to a pygeoapi config |

### `pygeoapi-config`

When set, the action reads every `type: feature` provider in the config
(including `id_field` values inherited through YAML anchors) and creates a
B-tree index on each table's `id_field` before running `pg_dump`, so
`/collections/{c}/items/{id}` lookups don't scan the whole table. The indexes
ship inside the dump as `CREATE INDEX ... USING btree` statements.

The step fails if a table named in the config is not in the database.

```yaml
- uses: cgs-earth/hydrodump-action@master
  with:
    username: ${{ secrets.HYDRO_USERNAME }}
    password: ${{ secrets.HYDRO_PASSWORD }}
    pygeoapi-config: pygeoapi.config.yml
```

The config must be checked out in the calling job before this action runs.
