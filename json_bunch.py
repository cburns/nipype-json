"""Explore using json for storing hashed inputs data to a file.
Currently we're storing the repr output of Bunch in a file.  The
file's name is the md5 hash of the repr.
"""

try:
    # json included in Python 2.6
    import json
except ImportError:
    # simplejson is the json module that was included in 2.6 (I
    # believe).  Used here for Python 2.5
    import simplejson as json

from nipype.interfaces.base import Bunch

# This is the Bunch from Realign.spm from pipeline tutorial.  Added
# quotes around the path for cwd.
rlgn_bunch = Bunch(cwd='/home/cburns/data/nipype-tutorial/workingdir/_subject_id_s1/Realign.spm', flags=None, fwhm=None, infile=['/home/cburns/data/nipype-tutorial/data/s1/f3.nii', '/home/cburns/data/nipype-tutorial/data/s1/f5.nii', '/home/cburns/data/nipype-tutorial/data/s1/f7.nii', '/home/cburns/data/nipype-tutorial/data/s1/f10.nii'], interp=None, quality=None, register_to_mean=True, separation=None, weight_img=None, wrap=None, write=True, write_interp=None, write_mask=None, write_which=None, write_wrap=None, )

# Dump input dictionary to file
fn = 'realign_json.txt'
fp = file(fn, 'w')
json.dump(rlgn_bunch.__dict__, fp, sort_keys=True, indent=4)
fp.close()

# Load input dictionary from file
fp = file(fn, 'r')
rlgn = json.load(fp)
fp.close()

# Compare saved dictionary with original
def sorted_dict_pairs(adict):
    keys = adict.keys()
    keys.sort()
    return [(k, adict[k]) for k in keys]
rlgn_list = sorted_dict_pairs(rlgn)
bunch_list = sorted_dict_pairs(rlgn_bunch.__dict__)
assert rlgn_list == bunch_list

