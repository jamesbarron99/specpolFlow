#!/usr/bin/python3
#
#Read a set of FITS files, in the ESPaDOnS spectra format from the CADC
#Can be modified for other spectra formats,
#if you know the structure of the records in the FITS file.
import numpy as np
import astropy.io.fits as fits

def espadons(flist):
    """
    Convert a list of .fits files in the CADC ESPaDOnS format into
    text .s files

    The code provides two files in .s format:
    * The UPENA normalized spectrum, with automated radial velocity corrections from the telluric lines.
    * The UPENA normalized spectrum, witout the automated radial velocity correction, 
        and we apply the radial velocity correction determined from the normalized spectrum.  
        The reason behind this is that the UPENA automated radial velocity determination performed on 
        unnormalized spectra does not produce consistant results. 
    The files are written at the same path as the fits-format data, with the '.fits' stripped, 
    and 'n.s' and 'u.s' appended to the filename root. 

    :param flist: (list of strings) a list of ESPaDOnS filenames
    """
    for fname in flist:
        print('converting ', fname.strip())
        # striping of white spaces
        fnameOut = fname.strip()
        # removing the '.fits' from the end of the string, 
        # to create the root name for the output files. 
        fnameOut = fnameOut.rstrip('.fits')
        # open the fits file with astropy
        fitsSpec = fits.open(fname.strip())

        header = fitsSpec[0].header

        # Useful for debugging
        print('File format info')
        print(fitsSpec.info())
        print('Header information')
        print(repr(header))

        # We need to extract the radial velocity correction 
        # that was determined from the normalized spectrum,
        # so that we can apply it to the unnormalized spectrum

        # TODO!!!!
        
        # extracting the table of data (24 columns)
        specTab = fitsSpec[0].data

        # The normalized spectrum with radial velocity correction from telluric lines
        # is the first 6 columns
        wln = specTab[0]
        specIn = specTab[1]
        specVn = specTab[2]
        specN1n = specTab[3]
        specN2n = specTab[4]
        specSign = specTab[5]
    
        # The unnormalized spectrum *without* the radial velocity correction
        # from the telluric lines is the last of 4 data blocks
        wlu = specTab[18]
        specIu = specTab[19]
        specVu = specTab[20]
        specN1u = specTab[21]
        specN2u = specTab[22]
        specSigu = specTab[23]
    
        fitsSpec.close()

        # Now we apply the velocity correction 
        # wave = wave + wave*vel/c 
        
        outNorm = open(fnameOut+'n.s','w')
        for i in range(len(wln)):
            outNorm.write('%10.4f %11.4e %11.4e %11.4e %11.4e %11.4e\n' % (wln[i], specIn[i], specVn[i], specN1n[i], specN2n[i], specSign[i]))
        outNorm.close()
    
        outUNorm = open(fnameOut+'u.s','w')
        for i in range(len(wln)):
            outUNorm.write('%10.4f %11.4e %11.4e %11.4e %11.4e %11.4e\n' % (wlu[i], specIu[i], specVu[i], specN1u[i], specN2u[i], specSigu[i]))
        outUNorm.close()
        
        outHeader = open(fnameOut+'.out','w')
        outHeader.write(repr(header))
        outHeader.close()


#For running as a terminal program
if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description='Convert FITS file spectra from the ESPaDOnS CADC archive format to text .s files. Output files as [filename]n.s for the pipeline normalized spectra, [filename]u.s for unnormalized spectra, and [filename].out for header information.')
    parser.add_argument("observation", nargs='*', help='a list of FITS files to process.')
    args = parser.parse_args()

    flist=args.observation

    if flist == []:
        print('No files given')
    else:
        #Run the conversion funciton
        espadons(flist)

