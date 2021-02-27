"""
from yamldb import YamlDB
from yamldb import Query

db = YamlDB('path/to/db.yaml')
user = Query()
db.insert({'name': 'Gregor', 'age': 111})
db.search(User.name == 'Gregor')

[{'name': 'John', 'age': 22}]

"""
from yamldb.util import readfile
import oyaml as yaml


class YamlDB:

    def __init__(self, filename):
        self.filename = filename
        print (filename)

    def load(self, filename=None):
        name = filename or self.filename
        content = readfile(name)
        self.data = yaml.safe_load(content)

    def save(self, filename=None):
        name = filename or self.filename
        with open(name, "w") as stream:
            yaml.safe_dump(self.data, stream, default_flow_style=False)

    def query(self, **attributes):
        """
        queries the database with attributes that all must be matched.

        :param attributes: attribute value pairs , and
        :type attributes:
        :return: matching results
        :rtype: dict
        """
        pass

    def __repr__(self):
        pass

    def __getattr__(self, item):
        pass

    def __len__(self):
        pass

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        """
        A helper function for setting the default cloud in the config without
        a chain of `set()` calls.

        Usage:
            value = db.set('a.b.c.d', 'value')

        :param key: A string representing the value's path in the config.
        :param value: value to be set.
        """

        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        try:
            if "." in key:
                keys = key.split(".")
                #
                # create parents
                #
                parents = keys[:-1]
                location = self.data
                for parent in parents:
                    if parent not in location:
                        location[parent] = {}
                    location = location[parent]
                #
                # create entry
                #
                location[keys[len(keys) - 1]] = value
            else:
                self.data[key] = value

        except KeyError:
            path = self.config_path
            Console.error(
                "The key '{key}' could not be found in the yaml file '{path}'".format(
                    **locals()))
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)

        yaml_file = self.data.copy()
        self.save()

    def __getitem__(self, item):
        """
        gets an item form the dict. The key is . separated
        use it as follows get("a.b.c")
        :param item:
        :type item:
        :return:
        """
        try:
            if "." in item:
                keys = item.split(".")
            else:
                return self.data[item]
            element = self.data[keys[0]]
            for key in keys[1:]:
                element = element[key]
        except KeyError:
            path = self.config_path
            raise KeyError(f"The key '{item}' could not be found in the yaml file '{path}'")
        except Exception as e:
            print(e)
            raise ValueError("unkown error")
        return element

    def __delitem__(self, item):
        """
        #
        # BUG THIS DOES NOT WORK
        #
        gets an item form the dict. The key is . separated
        use it as follows get("a.b.c")
        :param item:
        :type item:
        :return:
        """
        try:
            if "." in item:
                keys = item.split(".")
            else:
                return self.data[item]
            element = self.data
            print(keys)
            for key in keys:
                element = element[key]
            del element
        except KeyError:
            path = self.config_path
            raise KeyError(f"The key '{item}' could not be found in the yaml file '{path}'")
        except Exception as e:
            print(e)
            raise ValueError("unkown error")

    '''
    def search(self, key, value=None):
        """
        search("cloudmesh.cloud.*.cm.active", True)
        :param key:
        :param value:
        :return:
        """
        flat = FlatDict(self.data, sep=".")
        result = flat.search(key, value)
        return result
    '''