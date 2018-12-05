#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""A simple wrapper of NASA's-HEASARC fpack funpack tools.

Usage:

    >>> import pyfpack
    >>> fpack = pyfpack.FPack()
    >>> fpack.pack("path/to/file.fits")
    >>> fpack.unpack("path/to/file.fits.fz", O="path/to/file.fit")

fpack is a utility program for optimally compressing FITS format images.
The companion funpack program restores the compressed file back to its original
state. These programs may be run from the host operating system command line
and are analogous to the gzip and gunzip utility programs, except that they are
specifically optimized for FITS format images and offer a wider choice of
compression options.

fpack uses the tiled image compression convention for storing the compressed
images. This convention can in principle support any number of of different
compression algorithms; currently GZIP, Rice, Hcompress, and the IRAF pixel
list compression algorithms have been implemented.

fpack also supports the tiled table compression convention for compressing
FITS binary tables, which generally provides significantly greater compression
than can be achieved by simply compressing the FITS file with gzip.

The main advantages of fpack compared to the commonly used technique of
externally compressing the whole FITS file with gzip are:

    - It is generally faster and offers better compression than gzip.
    - The FITS header keywords remain uncompressed for fast access.
    - Each HDU of a multi-extension FITS file is compressed separately, so it
      is not necessary to uncompress the entire file to read a single image in
      a multi-extension file.
    - Dividing the image into tiles before compression enables faster access to
      small subsections of the image.
    - The compressed image is itself a valid FITS file and can be manipulated
      by other general FITS utility software.
    - Lossy compression can be used for much higher compression in cases where
      it is not necessary to exactly preserve the original pixel values.
    - The CHECKSUM keywords are automatically updated to help verify the
      integrity of the files.
    - Software that supports the tiled image compression technique can directly
      read and write the FITS images in their compressed form.
    - Can also compress FITS binary tables using a newly proposed
      FITS convention. This is intended for experimental feasibility studies,
      not for general use.

More info: http://heasarc.nasa.gov/fitsio/fpack/

"""


#===============================================================================
# IMPORTS
#===============================================================================

import subprocess

#===============================================================================
# CONSTANTS
#===============================================================================

CMD_PACK = "fpack"

CMD_UNPACK = "funpack"


#===============================================================================
# ERROR
#===============================================================================

class FPackException(Exception):
    """
        Exception class allowing a exit_code parameter and member
        to be used when calling fpack or funpack to return exit code.
    """

    def __init__(self, msg, exit_code=None):
        super(FPackException, self).__init__(msg)
        self.exit_code = exit_code


#===============================================================================
# FUNCTIONS
#===============================================================================


def _clean_fits_filenames(ffiles):
    ffiles = [ffiles] if isinstance(ffiles, basestring) else ffiles
    return [ffile.strip() for ffile in ffiles if ffile.strip()]


def _prevent_interactive(fitsfiles):
    for fpath in fitsfiles:
        if fpath == "-":
            msg = "Interactive Mode is not allowed"
            raise FPackException(msg)


def _prevent_invalid_arguments(kw, *a):
    inter = set(kw).intersection(a)
    if inter:
        msg = "Invalid Parameters: {}".format(",".join(a))
        raise FPackException(msg)

def _proc_args(kw):
    proc = []
    for k, v in kw.items():
        if isinstance(v, bool) and not v:
            continue
        proc.append(u"-{}".format(k))
        if not isinstance(v, bool):
            proc.append(unicode(v))
    return proc


def _execute(cmd, ffiles, kw):
    fullcommand = [cmd] + _proc_args(kw) + [u"-v"] + ffiles
    proc = subprocess.Popen(
        fullcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = [x.decode("utf-8") for x in proc.communicate()]
    if proc.returncode:
        fullcommand = u" ".join(fullcommand)
        raise FPackException(u"Error running %s:\n\" + "
                          u"tErr: %s\n\t"
                          u"Out: %s\n\t"
                          u"Exit: %s"
                          % (fullcommand, err, out, proc.returncode),
                          exit_code=proc.returncode)
    return out


def pack(fits_files, **kw):
    ffiles = _clean_fits_filenames(fits_files)
    _prevent_interactive(ffiles)
    _prevent_invalid_arguments(kw, "H", "V", "v", "S", "L", "C")
    return _execute(CMD_PACK, ffiles, kw)


def unpack(fits_files, **kw):
    ffiles = _clean_fits_filenames(fits_files)
    _prevent_interactive(ffiles)
    _prevent_invalid_arguments(kw, "H", "V", "v", "S", "L", "C")
    return _execute(CMD_UNPACK, ffiles, kw)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
