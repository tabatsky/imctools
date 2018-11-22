#!/usr/bin/env python
# Copyright (C) 2018-2019 University of Zurich. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import argparse
import os
import pandas as pd
import imctools.io.mcdxmlparser as mcdmeta

SUFFIX_ACMETA = '_' + mcdmeta.ACQUISITION + mcdmeta.META_CSV
COL_MCD_ID = mcdmeta.ID
COL_ACID = mcdmeta.ACQUISITIONID
COL_ACSESSION = 'AcSession'
SUF_CSV = '.csv'
AC_META = 'acquisition_metadata'

"""
Reads all the acquisition metadata from the ome folders and concatenates them
to a csv that contains all the metadata.
"""

def _read_and_concat(fol_ome, suffix, idname):
    ac_names = os.listdir(fol_ome)
    dat = pd.concat([pd.read_csv(os.path.join(fol_ome, a, a+suffix)) for a in ac_names],
                           keys=ac_names, names=[COL_ACSESSION])
    dat = dat.reset_index(COL_ACSESSION, drop=False)
    dat = dat.rename(columns={COL_MCD_ID: COL_ACID})
    return dat

def read_acmeta(fol_ome):
    dat_acmeta = _read_and_concat(fol_ome, SUFFIX_ACMETA, COL_ACID)
    return dat_acmeta

def export_acquisition_csv(fol_ome, fol_out, outname=AC_META):
    dat_meta = read_acmeta(fol_ome)
    dat_meta.to_csv(os.path.join(fol_out, outname+SUF_CSV), index=False)


if __name__ == "__main__":
    # Setup the command line arguments
    parser = argparse.ArgumentParser(
        description='Generates a metadatacsv for all acquisitions', prog='exportacquisitioncsv')

    parser.add_argument('fol_ome', type=str,
                        help='The path to the folders containing the ome tiffs.')

    parser.add_argument('out_folder', type=str,
                        help='Folder where the metadata csv should be stored in.')

    parser.add_argument('--outname', type=str, default=AC_META,
                        help='Filename of the acquisition metadata csv')

    args = parser.parse_args()

    export_acquisition_csv(args.fol_ome, args.out_folder,
                 args.outname)
