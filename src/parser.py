import os

from bs4 import BeautifulSoup


__author__ = 'deepak'


def start(owl_content):
    soup = BeautifulSoup(owl_content)
    classes = soup.find_all('owl:class')
    ids = {}
    abts = {}
    for x in classes:
        if 'rdf:id' in x.attrs:
            if x.get('rdf:id') in ids:
                ids[x.get('rdf:id')].append(x)
            else:
                ids[x.get('rdf:id')] = [x]
        if 'rdf:about' in x.attrs:
            if x.get('rdf:about').split("#")[-1] in abts:
                abts[x.get('rdf:about').split("#")[-1]].append(x)
            else:
                abts[x.get('rdf:about').split("#")[-1]] = [x]
    return ids, abts


def get_eqc(xml):
    soup = BeautifulSoup(str(xml))
    eqc = soup.find('owl:equivalentclass')
    if eqc:
        if 'rdf:resource' in eqc.attrs:
            return eqc.attrs.get('rdf:resource').split('#')[-1]
        else:
            soup = BeautifulSoup(str(eqc))
            if soup:
                owl_class = soup.find('owl:class') if soup else None
                if owl_class and 'rdf:about' in owl_class.attrs:
                    return owl_class.attrs.get('rdf:about').split('#')[-1]
                else:
                    return ''
            else:
                return ''
    else:
        return ''


def get_sc(xml):
    sc = []
    soup = BeautifulSoup(str(xml))
    for sub_class in soup.find_all('rdfs:subclassof'):
        owl_class = sub_class.find('owl:class')
        if 'rdf:resource' in sub_class.attrs:
            sc.append(sub_class.attrs.get('rdf:resource').split('#')[-1])
        elif owl_class:
            if owl_class.attrs.get('rdf:id'):
                sc.append(owl_class.attrs.get('rdf:id'))
            elif owl_class.attrs.get('rdf:about'):
                sc.append(owl_class.get('rdf:about').split('#')[-1])
        else:
            sc.append('')
    for intersection_class in soup.find_all('owl:intersectionof'):
        owl_class = intersection_class.find("owl:class")
        if owl_class and 'rdf:about' in owl_class.attrs:
            sc.append(owl_class.attrs.get('rdf:about').split("#")[-1])
        elif owl_class and 'rdf:id' in owl_class.attrs:
            sc.append(owl_class.attrs.get('rdf:id'))
    sc = list(set(sc))
    if '' in sc:
        sc.pop(sc.index(''))
    return sc


def classify(*args):
    subclasses = {}
    superclass = {}
    eq_class = {}
    for x in args:
        for k, xmls in x.items():
            for xml in xmls:
                eq = get_eqc(xml)
                if eq:
                    eq_class[k] = eq
                scs = get_sc(xml)
                if scs:
                    for sc in scs:
                        superclass[k] = sc
                        if sc in subclasses:
                            subclasses[sc].append(k)
                        else:
                            subclasses[sc] = [k]
                else:
                    subclasses['Thing'] = [k]
                    superclass[k] = 'Thing'
    return subclasses, superclass, eq_class


def parse(filename):
    filename = os.path.expanduser(filename)
    data = open(filename, "r").read()
    ids, abt = start(data)
    return classify(ids, abt)
