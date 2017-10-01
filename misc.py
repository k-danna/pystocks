
from math import floor

#pretty print json object
def print_json(json, depth=1):
    #fields to ignore, types convertable to string
    ignore = ['LogoUrl', 'IsSponsored', 'Created', 'Notice']
    printable = [str, unicode, bool, float, int, None]

    #indent a string n times
    def indent(string, n):
        for i in range(n):
            print '    ',
        print string

    #deal with json parsing issue
    if type(json) is list:
        for sub_obj in json:
            print_json(sub_obj, depth)
        return

    #recursive print
    indent('{', depth - 1)
    for key in json:
        if key in ignore:
            continue
        obj = json[key]
        obj_type = type(obj)
        if obj_type is dict:
            indent('%s: ' % key, depth)
            print_json(obj, depth + 2)
        elif obj_type is list:
            indent('%s: ' % key, depth)
            for sub_obj in obj:
                print_json(sub_obj, depth + 2)
        elif obj_type in printable:
            s = obj if obj else 'None'
            indent('%s: %s' % (key, s), depth)
        else:
            indent('%s: ERROR \'%s\'' % (key, obj_type), depth)
    indent('}', depth - 1)

#debug print with symbol type
def msg(string, symbol='*'):
    print '[%s] %s' % (symbol, string)


