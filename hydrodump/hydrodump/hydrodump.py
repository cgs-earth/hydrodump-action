# =================================================================
#
# Authors: Benjamin Webb <bwebb@lincolninst.edu>
#
# Copyright (c) 2023 Benjamin Webb
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================\

import click
from hsclient import HydroShare
import multiprocessing as mp
from pathlib import Path
import os
from tempfile import TemporaryDirectory
from time import sleep
from shutil import copy, unpack_archive
import subprocess

HYDRO_RESOURCE = os.getenv('HYDRO_RESOURCE')
HYDRO_USERNAME = os.getenv('HYDRO_USERNAME')
HYDRO_PASSWORD = os.getenv('HYDRO_PASSWORD')
HYDRO_DATADIR = Path('/data')

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'database')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

FILES_EXCLUDE = ['pws.csv', 'nldi_gages.geojson', 'e_merit_cats.gpkg',
                 'merit_plus_simplify.gpkg', 'pws.gpkg', 'gnis.zip',
                 'w_merit_cats.gpkg']


class HydroDump:
    def __init__(self) -> None:
        hs = HydroShare(HYDRO_USERNAME, HYDRO_PASSWORD)
        self.rs = hs.resource(HYDRO_RESOURCE)
        HYDRO_DATADIR.mkdir(parents=True, exist_ok=True)

    def files(self) -> list:
        return self.rs.files()

    def download(self, filename: str) -> None:
        if (HYDRO_DATADIR / filename).exists():
            return

        with TemporaryDirectory() as tmp:
            file = self.rs.file_download(filename, save_path=tmp, zipped=True)
            unpack_archive(file)
            copy(Path(filename) / filename, HYDRO_DATADIR)

    def transform(self, filename: str) -> None:
        file = HYDRO_DATADIR / filename
        command = ('ogr2ogr '
                   '-f "PostgreSQL" '
                   f'PG:"dbname={POSTGRES_DB} host={POSTGRES_HOST} port={POSTGRES_PORT} user={POSTGRES_USER} password={POSTGRES_PASSWORD}" '  # noqa
                   f'{file} -nln "{file.stem}" -lco OVERWRITE=yes')
        try:
            subprocess.run(str(command), check=True, shell=True)
        except subprocess.CalledProcessError as err:
            print(err)


def handle(f):
    hd = HydroDump()
    hd.download(f)
    hd.transform(f)
    print(f'{f.name} {f.checksum}')


@click.command()
@click.pass_context
def run(ctx):
    hd = HydroDump()
    spawnable = 2 if mp.cpu_count() == 1 else mp.cpu_count()

    for f in hd.files():
        if f in FILES_EXCLUDE:
            continue

        while len(mp.active_children()) == spawnable:
            sleep(0.1)

        p = mp.Process(target=handle, args=(f,))
        p.start()
