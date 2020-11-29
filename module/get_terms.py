from dataclasses import dataclass, field
from typing import List, Generator
from ete3 import NCBITaxa


def default_field(obj):
    return field(default_factory=lambda: obj)


@dataclass
class SynChem:
    """Dataclass with all the relevant chemical componds name"""

    sulfate: List[str] = default_field(['sulfate', 'so42-'])
    sodium: List[str] = default_field(['sodium', 'na+', 'na(i'])
    potassium: List[str] = default_field(['potassium', 'k+', 'k(i'])
    chloride: List[str] = default_field(['chloride', 'cl-'])
    carbonate: List[str] = default_field(['carbonate', 'hco3-'])
    magnesium: List[str] = default_field(['magnesium', 'mg2+', 'mg(ii'])
    calcium: List[str] = default_field(['calcium', 'ca2+', 'ca(ii'])
    copper: List[str] = default_field(['copper', 'cu2+', 'cu(ii'])
    iron: List[str] = default_field(
        ['iron', 'fe3+', 'fe(iii', 'fe2+', 'fe(ii'])
    zinc: List[str] = default_field(['zinc', 'zn2+', 'zn(ii'])
    cadmium: List[str] = default_field(['cadmium', 'cd2+', 'cd(ii'])
    arsenic: List[str] = default_field(['arsenic', 'as3+', 'as(iii', 'as(v'])
    lithium: List[str] = default_field(['lithium', 'li+', 'li(i'])
    boron: List[str] = default_field(['boron', 'b3+', 'b(iii'])
    manganese: List[str] = default_field(
        ['manganese', 'mn2+', 'mn4+', 'mn(ii', 'mn(iv'])
    phosphate: List[str] = default_field(['phosphate', 'po42-'])
    ammonium: List[str] = default_field(['ammonium', 'nh4+'])
    nitrite: List[str] = default_field(['nitrite', 'no2-'])
    nitrate: List[str] = default_field(['nitrate', 'no3-'])
    sulfide: List[str] = default_field(['sulfide', 'hs-'])
    methane: List[str] = default_field(['methane', 'ch4'])
    ethane: List[str] = default_field(['ethane', 'c2h6'])
    propane: List[str] = default_field(['propane', 'c3h8'])
    butane: List[str] = default_field(['butane', 'c4h10'])
    pentane: List[str] = default_field(['pentane', 'c5h12'])
    acetate: List[str] = default_field(['acetate', 'ch3coo-'])
    formate: List[str] = default_field(['formate', 'choo-'])
    pahs: List[str] = default_field(
        ['phenanthrene', 'naphthalene', 'anthracene', 'pyrene'])
    argon: List[str] = default_field(['argon', 'ar'])
    carbon_dioxyde: List[str] = default_field(['carbon_dioxyde', 'co2'])
    nitrogen: List[str] = default_field(['nitrogen', 'n2'])
    hydrogen: List[str] = default_field(['hydrogen', 'h2'])
    helium: List[str] = default_field(['helium', 'he'])


class SynTax:
    """Dataclass with all the relevant taxonomy"""
    def __init__(self):
        self.ncbi = NCBITaxa()

    def get_descendants(self, taxon_rank: str) -> Generator[str, None, None]:
        """Fetch all the available taxids"""
        taxids = self.ncbi.get_descendant_taxa('Bacteria',
                                               rank_limit=taxon_rank,
                                               collapse_subspecies=True)
        taxa_names = (self.ncbi.get_taxid_translator([taxa])
                      for taxa in taxids)
        return [values for i in taxa_names for key, values in i.items()]


@dataclass
class SynGeo:
    """Class dedicated to geological data"""
    geo_time: List[str] = default_field([
        'halocene', 'pleistocene', 'pliocene', 'miocene', 'oligocene',
        'eocene', 'paleocene', 'cretaceous', 'jurassic', 'triassic'
    ])

    minerals: List[str] = default_field([
        'minerals', 'calcite', 'pyrite', 'muscovite', 'feldspar', 'quartz',
        'kaolinite', 'illite', 'montmorillonite'
    ])


@dataclass
class SynMud:
    """Class dedicated to mud volcano specific data"""
    place: List[str] = default_field(['terrestrial', 'marine'])

    morphology: List[str] = default_field(
        ['cone', 'gryphones', 'cladera', 'salse'])

    methane_type: List[str] = default_field(['thermogenic', 'biogenic'])

    metabolics: List[str] = default_field(
        ['aom', 'srb', 'anammox', 'methanogenesis'])

    damo: List[str] = default_field(['s-damo', 'n-damo', 'm-damo'])

    type_methanogenesis: List[str] = default_field(
        ['acetoclastic', 'hydrogenoclastic', 'methyloclastic'])

    anme: List[str] = default_field(['anme', 'anme-1', 'anme-2', 'anme-3'])


@dataclass
class SynMethod:
    """Class dedicated to methods"""
    mineralogy: List[str] = default_field(
        ['x-ray diffraction', 'aes', 'empa', 'pixe', 'pige'])

    pcr: List[str] = default_field([
        'pcr', 'qpcr', 'rt-pcr', 'inverse pcr', 'nested pcr', 'mlpa',
        'hot start pcr', 'oe-pcr'
    ])
    genes: List[str] = default_field([
        'mcra', 'pmoa', 'dsrb', '16s', 'apra', 'nifh', 'alkl', 'alma', 'lada',
        'ebda', 'assa', 'bssa', 'nmsa'
    ])

    omics: List[str] = default_field(
        ['metagenomics', 'metabarcoding', 'transcriptomics', 'proteomics'])

    sequencing: List[str] = default_field(
        ['illumina', 'smrt', 'nanopore', 'pyrosequencing'])

    chromatography: List[str] = default_field(
        ['gc', 'gc-ms', 'hplc', 'gc-irms'])

    spectrometry: List[str] = default_field([
        'ftir', 'raman', 'icp-ms', 'lc-ms', 'uv-vis',
        'fluorescence spectrometry', 'column chromatography',
        'affinity chromatography', 'maldi'
    ])

    microscopy_staining: List[str] = default_field([
        'dapi', 'card-fish', 'fish', 'fish-nanosims', 'dark-field microscopy',
        'phase contrast', 'nanosims', 'sem', 'tem'
    ])

    microbiology: List[str] = default_field(
        ['culture', 'flow cytometry', 'sip'])

    blots: List[str] = default_field(
        ['southern blot', 'eastern blot', 'northern blot', 'western blot'])

    electrophoresis: List[str] = default_field(
        ['dgge', 'tgge', 'agarose gel electrophoresis', 'page'])

    core: List[str] = default_field(['ph', 'salinity', 'conductivity'])
