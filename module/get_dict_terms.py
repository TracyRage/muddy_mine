from .get_terms import SynChem, SynMud, SynGeo  # type: ignore
from .get_terms import SynMethod, SynTax  # type: ignore
from dataclasses import dataclass, field
from typing import Dict
"""Synopsis: get_dict_terms module aggregates all the Syn* dataclasses
into five distinct fields of interests: <chemistry>, <methods>,
<geology>, <mud> volcanoes, and taxonomy."""


def default_field(obj):
    """Synopsis: Generic helper function used for aggregation"""
    return field(default_factory=lambda: obj)


@dataclass
class SynChemDict:
    """Synopsis: generalization of SynChem dataclass"""
    chemistry: Dict = default_field({
        'sulfate': SynChem().sulfate,
        'sodium': SynChem().sodium,
        'potassium': SynChem().potassium,
        'chloride': SynChem().chloride,
        'carbonate': SynChem().carbonate,
        'magnesium': SynChem().magnesium,
        'calcium': SynChem().calcium,
        'copper': SynChem().copper,
        'iron': SynChem().iron,
        'zinc': SynChem().zinc,
        'cadmium': SynChem().cadmium,
        'arsenic': SynChem().arsenic,
        'lithium': SynChem().lithium,
        'boron': SynChem().boron,
        'manganese': SynChem().manganese,
        'phosphate': SynChem().phosphate,
        'ammonium': SynChem().ammonium,
        'nitrite': SynChem().nitrite,
        'nitrate': SynChem().nitrate,
        'sulfide': SynChem().sulfide,
        'methane': SynChem().methane,
        'ethane': SynChem().ethane,
        'propane': SynChem().propane,
        'butane': SynChem().butane,
        'pentane': SynChem().pentane,
        'acetate': SynChem().acetate,
        'formate': SynChem().formate,
        'pahs': SynChem().pahs,
        'argon': SynChem().argon,
        'carbon_dioxyde': SynChem().carbon_dioxyde,
        'nitrogen': SynChem().nitrogen,
        'hydrogen': SynChem().hydrogen,
        'helium': SynChem().helium,
    })


@dataclass
class SynGeoDict:
    """Synopsis: Generalisation of SynGeo dataclass"""
    geology: Dict = default_field({
        'geo_time': SynGeo().geo_time,
        'minerals': SynGeo().minerals,
    })


@dataclass
class SynMudDict:
    """Synopsis: Generalisation of SynMud dataclass"""
    mud: Dict = default_field({
        'place': SynMud().place,
        'morphology': SynMud().morphology,
        'methane_type': SynMud().methane_type,
        'metabolics': SynMud().metabolics,
        'damo': SynMud().damo,
        'type_mathanogenesis': SynMud().type_methanogenesis,
        'anme': SynMud().anme,
    })


@dataclass
class SynMethodDict:
    """Synopsis: Generalisation of SynMethod dataclass"""
    methods: Dict = default_field({
        'mineralogy': SynMethod().mineralogy,
        'pcr': SynMethod().pcr,
        'genes': SynMethod().genes,
        'omics': SynMethod().omics,
        'sequencing': SynMethod().sequencing,
        'chromatography': SynMethod().chromatography,
        'spectrometry': SynMethod().spectrometry,
        'microscopy_staining': SynMethod().microscopy_staining,
        'microbiology': SynMethod().microbiology,
        'blots': SynMethod().blots,
        'electrophoresis': SynMethod().electrophoresis,
        'core': SynMethod().core
    })


@dataclass
class SynTaxaDict:
    """Synopsis: Generalisation of SynTax class"""
    taxonomy: Dict = default_field({'tax': SynTax()})
