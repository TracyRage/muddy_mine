from dataclasses import dataclass, field
from typing import Sequence, Tuple


def default_field(obj):
    return field(default_factory=lambda: obj)


@dataclass
class SynChem:
    """Dataclass with all the relevant chemicals' names"""

    ions: Sequence[Tuple[str]] = default_field([
        ('sulfate', 'so42-'),
        ('sodium', 'na+'),
        ('chloride', 'cl-'),
        ('carbonate', 'hco3-'),
        ('magnesium', 'mg2+'),
        ('iron', 'fe3+'),
        ('arsenic', 'as3+'),
        ('lithium', 'li+'),
        ('boron', 'b3+'),
        ('phosphate', 'po42-'),
        ('ammonium', 'nh4+'),
        ('nitrite', 'no2-'),
        ('nitrate', 'no3-'),
        ('sulfide', 'hs-'),
    ])

    alkanes_organics: Sequence[Tuple[str]] = default_field([
        ('methane', 'ch4'),
        ('ethane', 'c2h6'),
        ('propane', 'c3h8'),
        ('butane', 'c4h10'),
        ('ethane', 'c5h12'),
        ('acetate', 'ch3coo-'),
        ('formate', 'choo-'),
    ])

    pahs: Sequence[Tuple[str]] = default_field([
        ('phe', 'phenanthrene'),
        ('naph', 'naphthalene'),
        ('anth', 'anthracene'),
        ('pyr', 'pyrene'),
    ])

    gases: Sequence[Tuple[str]] = default_field([
        ('carbon dioxyde', 'co2'),
        ('nitrogen', 'n2'),
        ('hydrogen', 'h2'),
        ('helium', 'he'),
    ])


@dataclass
class SynTax:
    """Dataclass with all the relevant taxonomy"""

    phylum_suffix: Sequence[str] = default_field([
        'ria', 'gae', 'diae', 'xi', 'tes', 'res', 'cia', 'bi', 'bia', 'spira',
        'spirae'
    ])

    family_suffix: Sequence[str] = default_field(['aceae'])

    order_suffix: Sequence[str] = default_field(['ales'])

    class_suffix: Sequence[str] = default_field(['ia'])

    archaea_type: Sequence[Tuple[str]] = default_field([
        ('anme-1', 'anme-1a', 'anme-1b'),
        ('anme-2', 'anme-2a', 'anme-2b', 'anme-3b', 'anme-4d'),
        ('anme-3'),
    ])


@dataclass
class SynGeo:
    """Class dedicated to geological data"""
    geo_time: Sequence[str] = default_field([
        ('periods', 'halocene', 'pleistocene', 'pliocene', 'miocene',
         'oligocene', 'eocene', 'paleocene', 'cretaceous', 'jurassic',
         'triassic')
    ])

    minerals: Sequence[Tuple[str]] = default_field([
        ('calcite', 'py'),
        ('pyrite', 'cal'),
        ('muscovite', 'ms'),
        ('feldspar', 'kfs'),
        ('quartz', 'qz'),
        ('kaolinite', 'kao'),
        ('illite', 'ill'),
        ('montmorillonite', 'mm'),
    ])


@dataclass
class SynMud:
    """Class dedicated to mud volcano specific data"""
    place: Sequence[str] = default_field(['terrestrial', 'marine'])

    morphology: Sequence[str] = default_field([
        ('cone', 'cones'),
        ('gryphon', 'gryphons'),
        ('pie', 'pies'),
        ('cladera', 'calderas'),
        ('salse', 'salses'),
    ])

    methane_type: Sequence[str] = default_field([(
        'methane_type',
        'thermogenic',
        'biogenic',
    )])

    metabolics: Sequence[str] = default_field([
        ('metabolism', 'aom', 'srb', 'anammox', 'methanogenesis'),
    ])

    damo: Sequence[str] = default_field([
        ('damo', 's-damo', 'n-damo', 'm-damo'),
    ])

    type_methanogenesis: Sequence[str] = default_field([
        ('type_methanogenesis', 'acetoclastic', 'hydrogenoclastic'),
    ])


@dataclass
class SynMethod:
    """Class dedicated to methods"""
    methods: Sequence[str] = default_field([
        ('diffraction', 'x-ray'),
        ('pcr', 'qpcr', 'rt-pcr'),
        ('genomics', 'metagenomics', 'metabarcoding', 'transcriptomics'),
        ('spectrometry', 'gc', 'gc-ms', 'hplc', 'gs-irms', 'icp-ms'),
        ('microscopy', 'dapi', 'card-fish', 'fish'),
        ('culture', 'cultures'),
        ('gene', 'mcra', 'pmoa', 'dsrb', '16s'),
        ('electrophoresis', 'dgge'),
        ('core', 'ph', 'salinity'),
    ])


if __name__ == "__main__":
    record = SynChem()
    print(record.ions)
