# ceremaAWP
Python notebook to import the Cerema AWP dataset in hdf5 format

The Cerema AWP (Adverse Weather Pedestrian) can be downloaded at https://ceremadlcfmds.wixsite.com/cerema-databases.

The proposed script here let you import in one single hdf5 file all images and labels, split into train and test sets (0.15% of the images in the test set), with an equivalent proportion of each class in train and test.
Images can be resized be setting a proportion parameter, and cropped to be squared.


# help
usage: exportCeremaAWP.py [-h] [-s] [-p PROP] [-o OUTPUTFILE]

CeremaAWP Parser

optional arguments:
  -h, --help     show this help message and exit
  -s             Requires to crop images to get squares
  -p PROP        Proportion of initial size for resizing (default 0.25)
  -o OUTPUTFILE  Output file (default CeremaAWP0.25.hdf5)
