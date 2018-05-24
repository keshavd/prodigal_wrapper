class PrismBinner(object):

    def __init__(self):
        pass

    @staticmethod
    def get_json_list(json_dir):
        from glob import glob
        import os
        list_of_jsons = glob("%s%s*.json" % (json_dir, os.sep)
        return list_of_jsons

    def sort(self, json_dir):
        from mlab.PrismBuilder import PrismBuilder
        pb = PrismBuilder()
        families = dict()
        list_of_jsons = self.get_json_list(json_dir)
        for result in list_of_jsons:
            a = pb.ResultFromJson(result)
            for cluster in a.clusters:
                try:
                    fam = cluster.family
                    for f in fam:
                        families[f].append(cluster)
                except KeyError:
                    families[f] = list()
                    families[f].append(cluster)
        subbinned = dict()
        for family_name, bgcs in families.items():
            subbinned[family_name] = dict()
            for bgc in bgcs:
                modules = 0
                for orf in bgc.orfs:
                    all_modules=[]
                    domains = orf.raw_domains
                    if domains is not None:
                        for domain in domains:
                            on_module = domain['on_module']
                            if on_module:
                                all_modules.append(domain['module_number'])
                    l = len(set(all_modules))
                    modules += l
                try:
                    subbinned[family_name][modules].append(bgc)
                except KeyError:
                    subbinned[family_name][modules] = list()
                    subbinned[family_name][modules].append(bgc)
        return subbinned