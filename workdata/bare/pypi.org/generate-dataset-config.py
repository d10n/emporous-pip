#!/usr/bin/env python
import json
import os

import pkginfo2
import yaml

from pkginfo2 import Wheel, SDist

dataset_config = yaml.safe_load("""
kind: DataSetConfiguration
apiVersion: client.uor-framework.io/v1alpha1
collection:
  files:
    - file: '*.whl'
      attributes:
        pyindex: true
    - file: '*.tar.gz'
      attributes:
        pyindex: true
""")
dataset_config = {
    'kind': 'DataSetConfiguration',
    'apiVersion': 'client.uor-framework.io/v1alpha1',
    'collection': {
        'files': [
            {
                'file': '*.whl',
                'attributes': {
                    'pyindex': True
                }
            },
            {
                'file': '*.tar.gz',
                'attributes': {
                    'pyindex': True
                }
            }
        ]
    }
}


def getmeta(pkgpath):
    if pkgpath.endswith('.tar.gz'):
        dist = pkginfo2.SDist
    elif pkgpath.endswith('.whl'):
        dist = pkginfo2.Wheel
    else:
        dist = None
    if dist:
        pkg = dist(pkgpath)
        # print(pkg.name, pkg.license)
        return pkg
    pass

for root, dirs, files in os.walk('./simple'):
    # print([root, dirs, files])

    for file in files:
        if file.endswith(('.tar.gz', '.whl')):
            filepath = os.path.join(root, file)
            meta = getmeta(filepath)
            if meta:
                filtered_meta = {
                    k: v for k, v in vars(meta).items()
                    if k != 'filename' and v}
                filtered_meta = {
                    k: json.dumps(v) if not isinstance(v, (bool, int, float, str)) else v
                        for k, v in filtered_meta.items()}
                filtered_meta['package'] = filtered_meta['name']

                dataset_config['collection']['files'].extend([
                    {
                        'file': filepath.removeprefix('./simple/'),
                        'attributes': filtered_meta
                    }
                ])
            pass

    pass

print(yaml.safe_dump(dataset_config, sort_keys=False))
# print(dataset_config)
pass