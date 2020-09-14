# Author: Avimitin
# Date: 2020/09/14

class OPT:
    def __init__(self,
                 name,
                 paolu=False,
                 debug=False,
                 test_method=None,
                 test_mode=None,
                 confirmation=True,
                 result_color=None,
                 import_file=False,
                 guiConfig=None,
                 url=None,
                 filter=None,
                 group=None,
                 remarks=None,
                 efliter=None,
                 egfilter=None,
                 erfilter=None,
                 sort_method=None,
                 group_override=None,
                 use_ssr_CSharp=False,
                 skip_requirements_check=True
                 ):
        self.name = name
        self.paolu = paolu
        self.debug = debug
        self.test_method = test_method
        self.test_mode = test_mode
        self.confirmation = confirmation
        self.result_color = result_color
        self.import_file = import_file
        self.guiConfig = guiConfig
        self.url = url
        self.filter = filter
        self.group = group
        self.remarks = remarks
        self.efliter = efliter
        self.egfilter = egfilter
        self.erfilter = erfilter
        self.sort_method = sort_method
        self.group_override = group_override
        self.use_ssr_cs = use_ssr_CSharp
        self.skip_requirements_check = skip_requirements_check