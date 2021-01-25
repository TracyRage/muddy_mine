from dataclasses import dataclass, field
from typing import List
from ete3 import NCBITaxa  # type: ignore


def default_field(obj):
    """Synopsis: Generic helper function
    used for aggregation"""
    return field(default_factory=lambda: obj)


@dataclass
class SynChem:
    """Synopsis: SynChem dataclass contains all the
    relevant chemical tokens to mine"""
    # Ions
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
    # Alkanes
    methane: List[str] = default_field(['methane', 'ch4'])
    ethane: List[str] = default_field(['ethane', 'c2h6'])
    propane: List[str] = default_field(['propane', 'c3h8'])
    butane: List[str] = default_field(['butane', 'c4h10'])
    pentane: List[str] = default_field(['pentane', 'c5h12'])
    # Organic acids
    acetate: List[str] = default_field(['acetate', 'ch3coo-'])
    formate: List[str] = default_field(['formate', 'choo-'])
    # PAHs
    pahs: List[str] = default_field(
        ['phenanthrene', 'naphthalene', 'anthracene', 'pyrene'])
    # Gases
    argon: List[str] = default_field(['argon', 'ar'])
    carbon_dioxyde: List[str] = default_field(['carbon_dioxyde', 'co2'])
    nitrogen: List[str] = default_field(['nitrogen', 'n2'])
    hydrogen: List[str] = default_field(['hydrogen', 'h2'])
    helium: List[str] = default_field(['helium', 'he'])


class SynTax:
    """Synopsis: SynTax class contains all the relevant taxonomy to mine"""
    def __init__(self):
        self.ncbi = NCBITaxa()

    def get_descendants(self, domain: str, taxon_rank: str) -> List[str]:
        """Synopsis: Fetch all the available taxids"""
        # Domain must be in title case
        taxids = self.ncbi.get_descendant_taxa(domain,
                                               rank_limit=taxon_rank,
                                               collapse_subspecies=True)
        taxa_names = (self.ncbi.get_taxid_translator([taxa])
                      for taxa in taxids)
        return [values for i in taxa_names for key, values in i.items()]


@dataclass
class SynGeo:
    """Synopsis: SynGeo dataclass contains all the relevant
    geological data to mine"""
    # Geological time scale
    geo_time: List[str] = default_field([
        'halocene', 'pleistocene', 'pliocene', 'miocene', 'oligocene',
        'eocene', 'paleocene', 'cretaceous', 'jurassic', 'triassic'
    ])
    # Minerals
    minerals: List[str] = default_field([
        'calcite', 'pyrite', 'muscovite', 'feldspar', 'quartz', 'kaolinite',
        'illite', 'montmorillonite'
    ])


@dataclass
class SynMud:
    """Synopsis: SynMud dataclass contains all the
    relevant mud volcano terminology to mine"""
    # Mud volcano spacial placement
    place: List[str] = default_field(['terrestrial', 'marine'])
    # Mud volcano morphology
    morphology: List[str] = default_field(
        ['cone', 'gryphones', 'cladera', 'salse'])
    # Methane origin
    methane_type: List[str] = default_field(['thermogenic', 'biogenic'])
    # Mud volcano typical metabolic pathways
    metabolics: List[str] = default_field(
        ['aom', 'srb', 'anammox', 'methanogenesis'])
    # DAMO pathways
    damo: List[str] = default_field(['s-damo', 'n-damo', 'm-damo'])
    # Methanogenesis types
    type_methanogenesis: List[str] = default_field(
        ['acetoclastic', 'hydrogenoclastic', 'methyloclastic'])
    # ANME classification
    anme: List[str] = default_field(['anme', 'anme-1', 'anme-2', 'anme-3'])


@dataclass
class SynMethod:
    """Synopsis: SynMethod dataclass contains all
    the relevant lab methods to mine"""
    # Mineralogical methods types
    mineralogy: List[str] = default_field(
        ['x-ray diffraction', 'aes', 'empa', 'pixe', 'pige'])
    # PCR types
    pcr: List[str] = default_field([
        'pcr', 'qpcr', 'rt-pcr', 'inverse pcr', 'nested pcr', 'mlpa',
        'hot start pcr', 'oe-pcr'
    ])
    # Genes amplified / analyzed
    genes: List[str] = default_field([
        'mcra', 'pmoa', 'dsrb', '16s', 'apra', 'nifh', 'alkl', 'alma', 'lada',
        'ebda', 'assa', 'bssa', 'nmsa'
    ])
    # *omics types implied
    omics: List[str] = default_field(
        ['metagenomics', 'metabarcoding', 'transcriptomics', 'proteomics'])
    # Sequencing types
    sequencing: List[str] = default_field(
        ['illumina', 'smrt', 'nanopore', 'pyrosequencing'])
    # Chromatography types
    chromatography: List[str] = default_field(
        ['gc', 'gc-ms', 'hplc', 'gc-irms'])
    # Spectrometry types
    spectrometry: List[str] = default_field([
        'ftir', 'raman', 'icp-ms', 'lc-ms', 'uv-vis',
        'fluorescence spectrometry', 'column chromatography',
        'affinity chromatography', 'maldi'
    ])
    # Microscopy and staining types
    microscopy_staining: List[str] = default_field([
        'dapi', 'card-fish', 'fish', 'fish-nanosims', 'dark-field microscopy',
        'phase contrast', 'nanosims', 'sem', 'tem'
    ])
    # Microbiology methods types
    microbiology: List[str] = default_field(
        ['culture', 'flow cytometry', 'sip'])
    # Bloats types
    blots: List[str] = default_field(
        ['southern blot', 'eastern blot', 'northern blot', 'western blot'])
    # Electrophoresis types
    electrophoresis: List[str] = default_field(
        ['dgge', 'tgge', 'agarose gel electrophoresis', 'page'])
    # Core analysis types
    core: List[str] = default_field(['ph', 'salinity', 'conductivity'])
