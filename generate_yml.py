import csv
import numpy as np
import yaml
from yaml.loader import SafeLoader
import os
import pandas as pd

def read_template(file, verbose=False):
    with open(file) as t:
        template = yaml.load(t, Loader = SafeLoader)
        if verbose:
            print(f'Template has the following keys:{template.keys()}')
        return template

def create(**entries):
    """
    Function which creates an entry for the z10-galaxies repository.

    Example use:
    If you already have your values defined in a table tab loaded in memory, you can
    generate the YML entries like this:

    for id, ra, dec, z, fa, ref in zip(tab['id'],tab['ra'],tab['dec'],tab['z'],tab['fa'],tab['ref']):
        create(default_id = id, default_ra = ra, default_dec = dec,\ 
            default_phot_z = z, default_first_author = fa, default_ref = ref)

    """
    template_file = 'QSOs/TEMPLATE'
    template = read_template(template_file)

    default_keys = []
    for key in template.keys():
        if 'default' in key:
            default_keys.append(key)

    for key in default_keys:
        if key not in entries.keys():
            raise Warning(f'{key} must be defined')
            return

    for key, value in entries.items():
        try:
            template[key]['value'] = value
        except KeyError:
            print(f'{key} is not a valid key to this template')
            return

    outfile = f'{entries["default_ref"]}_{entries["default_name"]}.yml'
    print(f'Writing {outfile}')
    with open('QSOs/' + outfile, 'w') as f:
        data = yaml.dump(template, f)


# Load the table with the new QSOs
colnames = ['Quasar', 'ra', 'dec', 'redshift', 'redshift_reference', 'm1450','Mabs1450', 'redshift_mgii', 
       'redshift_mgii_err', 'redshift_mgii_ref', 'fwhm_mgii', 'fwhm_mgii_err_up', 'fwhm_mgii_err_low', 'L3000',
       'L3000err_up', 'L3000err_low', 'BHmass', 'BHmass_reference']

tab = pd.read_csv('AA61_Fan_qso_database.csv', sep = ',', names = colnames, skiprows = 2)


# Create yml file for each source

for name, ra, dec, z, ref, m1450, M1450, z_mgii, z_mgii_err, z_mgii_ref, fwhm_mgii, fwhm_mgii_err_up, fwhm_mgii_err_low,  L3000, L3000_err_up, L3000_err_low, BHmass, BHmass_ref  in zip(tab['Quasar'],tab['ra'],tab['dec'],tab['redshift'], tab['redshift_reference'],tab['m1450'], \
          tab['Mabs1450'], tab['redshift_mgii'], tab['redshift_mgii_err'], tab['redshift_mgii_ref'], \
          tab['fwhm_mgii'], tab['fwhm_mgii_err_up'], tab['fwhm_mgii_err_low'], tab['L3000'], tab['L3000err_up'], \
          tab['L3000err_low'], tab['BHmass'], tab['BHmass_reference']):

        create(default_name = name, default_ra = ra, default_dec = dec, default_z = z, default_ref = ref, \
               photometry_m1450 = m1450, photometry_absM1450 = M1450, extra_z_mgii = z_mgii, \
               extra_z_mgii_err = z_mgii_err, extra_z_mgii_ref = z_mgii_ref, extra_fwhm_mgii = fwhm_mgii, \
               extra_fwhm_mgii_err_up = fwhm_mgii_err_up, extra_fwhm_mgii_err_low = fwhm_mgii_err_low, \
               extra_L3000 = L3000, extra_L3000_err_up = L3000_err_up, extra_L3000_err_low = L3000_err_low,\
               extra_BHmass = BHmass, extra_BHmass_ref = BHmass_ref)
