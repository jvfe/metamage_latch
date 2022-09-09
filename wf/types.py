from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json
from latch.types import LatchFile


@dataclass_json
@dataclass
class Sample:
    read1: LatchFile
    read2: LatchFile


@dataclass_json
@dataclass
class HostData:
    host_name: str
    host_genome: LatchFile


class TaxonRank(Enum):
    superkingdom = "superkingdom"
    phylum = "phylum"
    taxon_class = "class"
    order = "order"
    family = "family"
    genus = "genus"
    species = "species"


class ProdigalOutput(Enum):
    gbk = "gbk"
    gff = "gff"
    sco = "sco"


class fARGeneModel(Enum):
    class_a = "class_a"
    class_b_1_2 = "class_b_1_2"
    class_b_3 = "class_b_3"
    class_c = "class_c"
    class_d_1 = "class_d_1"
    class_d_2 = "class_d_2"
    qnr = "qnr"
    tet_efflux = "tet_efflux"
    tet_rpg = "tet_rpg"
    tet_enzyme = "tet_enzyme"
    erm_type_a = "erm_type_a"
    erm_type_f = "erm_type_f"
    mph = "mph"
    aminoglycoside_model_a = "aminoglycoside_model_a"
    aminoglycoside_model_b = "aminoglycoside_model_b"
    aminoglycoside_model_c = "aminoglycoside_model_c"
    aminoglycoside_model_d = "aminoglycoside_model_d"
    aminoglycoside_model_e = "aminoglycoside_model_e"
    aminoglycoside_model_f = "aminoglycoside_model_f"
    aminoglycoside_model_g = "aminoglycoside_model_g"
    aminoglycoside_model_h = "aminoglycoside_model_h"
    aminoglycoside_model_i = "aminoglycoside_model_i"
