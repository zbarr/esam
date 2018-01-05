import os
import yaml

exclude_directories = ['TSB_old_to_be_removed', 'operations', 'chicago_0', 'qa1', 'sample_yaml_app_files']


for root, dirs, files in os.walk("../salt-app/server-configs"):
    path = root.split(os.sep)

    if len(path) > 3:
        if not any(directory in path[3] for directory in exclude_directories):
            if any('yaml' in instance for instance in files):
                with open(root + "/" + files[0], 'r') as stream:
                    try:
                        yaml_dict = yaml.load(stream)
                        if yaml_dict:
                            if 'sapphire' in yaml_dict:

                                for engine, data in yaml_dict['sapphire'].items():
                                    datastring = files[0].split('.')[0] + " "
                                    datastring += engine + " "
                                    if 'desk' in data:
                                        datastring += data['desk']
                                    else:
                                        datastring += data['acc_desk']
                                    print (datastring)


                    except yaml.YAMLError as exc:
                        print(exc)


















"""
for root, dirs, files in os.walk("../salt-app/client-configs"):
    print (root)
    #print (dirs)
    #print (files)
    path = root.split(os.sep)

"""
