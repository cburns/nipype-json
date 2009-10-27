"""Explore using json for storing hashed inputs data to a file.
Currently we're storing the repr output of Bunch in a file.  The
file's name is the md5 hash of the repr.
"""
import copy
import hashlib

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

def add_hashes(adict, key):
    # Inject file hashes into adict[key]
    file_list = []
    for afile in adict[key]:
        md5obj = hashlib.md5()
        fp = file(afile, 'rb')
        md5obj.update(fp.read())
        fp.close()
        file_list.append((afile, md5obj.hexdigest()))
    return file_list

def remove_hashes(adict, key):
    # Remove hashes from adict[key]
    return [filename for filename, filehash in adict[key]]

inputs = copy.deepcopy(rlgn_bunch.__dict__)
inputs['infile'] = add_hashes(inputs, 'infile')

# Dump input dictionary to file
fn = 'realign_json.txt'
fp = file(fn, 'w')
json.dump(inputs, fp, sort_keys=True, indent=4)
fp.close()

# Load input dictionary from file
fp = file(fn, 'r')
rlgn_orig = json.load(fp)
fp.close()

# Remove hashes on reload to compare against original dictionary
rlgn = copy.deepcopy(rlgn_orig)
rlgn['infile'] = remove_hashes(rlgn, 'infile')

# Compare saved dictionary with original
def sorted_dict_pairs(adict):
    keys = adict.keys()
    keys.sort()
    return [(k, adict[k]) for k in keys]
rlgn_list = sorted_dict_pairs(rlgn)
bunch_list = sorted_dict_pairs(rlgn_bunch.__dict__)
assert rlgn_list == bunch_list

# Check for compatibility with YAML
# JSON should be a subset of YAML, try loading our json file with PyYAML
yaml_loaded = False
try:
    import yaml
    yaml_loaded = True
except ImportError:
    pass

if yaml_loaded:
    fp = file(fn)
    json_dict = json.load(fp)
    fp.seek(0)
    yaml_dict = yaml.load(fp)
    fp.close()
    json_list = sorted_dict_pairs(json_dict)
    yaml_list = sorted_dict_pairs(yaml_dict)
    assert json_list == yaml_list
