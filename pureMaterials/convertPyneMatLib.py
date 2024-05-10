#!/usr/bin/python
#
# -updated for python3 (print)
# -updated for changes in pyne python modules
#
#
import argparse
#from pyne import nuc_data # import the pre-built materials database for testing (this causes some file path name trouble so comment out)
from pyne.material_library import MaterialLibrary # import the material library class from the new location in recent versions of pyne
#
#
parser = argparse.ArgumentParser(description=(
             'Reads a pyne database file of material objects'))
parser.add_argument('-f', dest='filenamein', help='Name of the pyne material database file to read...specify full directory path e.g. -f /home/smith/.local/lib/python2.7/site-packages/pyne/nuc_data.h5 or -f testelliot/testlibsh6_70c.h5m')
parser.add_argument("-m","--writeMCNP", help="Write all materials in MCNP matl card format to 2 text files (atom and mass fraction)",action="store_true")
parser.add_argument("-c","--writeOpenMC", help="Write all materials in OpenMC matl format to 2 text files (atom and mass fraction)",action="store_true")
parser.add_argument("-l","--writeAlara", help="Write all materials in Alara matl card format to a text file",action="store_true")
parser.add_argument("-j","--writeJson", help="Write all materials in Json matl card format to individual files",action="store_true")
parser.add_argument("-p","--prebuilt", help="Assume prebuilt matl library distributed with PyNE that has non-default datapath,nucpath",action="store_true")
parser.add_argument("-w","--writedefault", help="Write out the library using default datapath,nucpath",action="store_true")
args = parser.parse_args()
#
pynematdatabasefilein=args.filenamein if args.filenamein is not None else "/home/smith/.local/lib/python2.7/site-packages/pyne/nuc_data.h5"
#
#
print("\n \n The pyne material database file is:", pynematdatabasefilein)
#
# read in materials database from the input file
if args.prebuilt:
    matllib = MaterialLibrary(lib=pynematdatabasefilein, datapath='/material_library/materials', nucpath='/material_library/nucid') # use specific datapath,nucpath
else:
    matllib = MaterialLibrary(lib=pynematdatabasefilein) # use default datapath,nucpath
#
print("\n The number of entries in the materials database: ", len(matllib))
#print "Some entries in the materials database: ", matllib.keys()[0:7]
# matllib.keys()[:7]
#
print("All the entries in the materials database: ")
for matkey, matvalue in matllib.items():
    print("   The key is: ", matkey.decode('utf8'), "The mass density is: ",matllib[matkey].mass_density(),"atom density","{:11.4e}".format(matllib[matkey].number_density()/1.0e24))
#
# prompt for a entry from the material database to print out information
input_string=input("\n Enter a material from the database to print out info: ")
print("The material requested is: \n", input_string)
#
print("\n Printing some entries from the database...")
print("   Material print of: ", input_string)
print("            molecular mass: ",matllib[input_string].molecular_mass(), " mass density: ", matllib[input_string].mass_density())
print("\n An mcnp material print of input_string using mass fractions...\n", matllib[input_string].mcnp()) # mass fraction is the default
print("\n An mcnp material print of input_string using atom fractions...\n", matllib[input_string].mcnp('atom')) # use atom fraction
print("\n    Writing the same to a json file (testplayjson.txt) and mcnp format file (testplaymat_mcard.txt) using atom fractions...\n")
testmat=matllib[input_string]
testmat.write_mcnp('testplaymcnp.txt', 'atom')
testmat.write_json('testplayjson.txt')
#
#
# if requested, write all the materials in MCNP matl card format to a text file
if args.writeMCNP:
    print("\n Writing all the materials in MCNP matl card format to 2 text files (atom and mass frac format)... \n")
    for matkey, matvalue in matllib.items():
        print("   Writing ", matkey.decode('utf8'), "to a file (testplayallmat_mcnpxxx.txt) using MCNP format and atom/mass fractions...  \n")
        testmat=matllib[matkey]
        testmat.write_mcnp('testplayallmat_mcnpAtomfrac.txt', 'atom')
        testmat.write_mcnp('testplayallmat_mcnpMassfrac.txt')
# if requested, write all the materials in OpenMC matl card format to a text file
if args.writeOpenMC:
    print("\n Writing all the materials in OpenMC material format (atom fraction)... \n")
    matllib.write_openmc("testplayallmat_openmcAtomfrac.xml")
#
# if requested, write all the materials in Alara matl card format to a text file
if args.writeAlara:
    print("\n Writing all the materials in Alara matl card format to a text file... \n")
    for matkey, matvalue in matllib.items():
        print("   Writing ", matkey.decode('utf8'), "to a file (testplayallmat_alara.txt) using Alara format ...  \n")
        testmat=matllib[matkey]
        testmat.write_alara('testplayallmat_alara.txt')
#
# if requested, write all the materials in Json matl card format to a text file
if args.writeJson:
    print("\n Writing all the materials in Json matl card format to a text file... \n")
    for matkey, matvalue in matllib.items():
        jsonFileName=matkey.decode('utf8')+".json"
        print("   Writing ", matkey.decode('utf8'), "to a file ",jsonFileName," using Json format ...  \n")
        testmat=matllib[matkey]
        testmat.write_json(jsonFileName) # doesn't append so only last material in list appears
#
# if requested, write the library with default datapath nucpath for uwuw workflow
if args.writedefault:
    print("\n Writing the library with default datapath,nucpath...")
    matllib.write_hdf5("testlibdefaultpaths.h5") # don't set datapath,nucpath...will be pyne default values
print("\n \n All done!")
