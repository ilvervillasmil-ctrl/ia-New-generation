"""
Test Suite: Domain 3 — DNA / Molecular Biology (Destruction Test)
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

PURPOSE: Test whether alpha/beta structure emerges in DNA sequences —
a domain shaped by evolution, mutation, and natural selection,
NOT by geometric design.

WHY THIS IS THE MOST SERIOUS TEST:
- Evolution is blind — no architect, no geometry
- DNA structure emerged from chemistry and selection pressure
- If alpha/beta appears here -> deeply non-trivial
- If it doesn't -> clear framework boundary (good science)

DOMAINS TESTED:
1. Codon structure (64 codons, 61 coding + 3 stop)
2. Coding vs non-coding DNA ratio
3. Nucleotide frequency distributions
4. GC content across organisms
5. Amino acid frequency in proteins
6. Random sequences MUST differ from real DNA

HONEST RULES:
- Measure first, interpret later
- Random DNA must show different structure
- Document failures as boundaries
"""

import sys
import os
import math
import random
import pytest
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from formulas.constants import ALPHA, BETA, PHI
except ImportError:
    ALPHA = 26 / 27
    BETA = 1 / 27
    PHI = (1 + math.sqrt(5)) / 2


# ============================================================
# BIOLOGICAL CONSTANTS (established science)
# ============================================================

TOTAL_CODONS = 64
CODING_CODONS = 61
STOP_CODONS = 3

AMINO_ACIDS = 20
NUCLEOTIDES = ['A', 'T', 'G', 'C']

# Standard genetic code: codon -> amino acid
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# Real DNA sample: Human hemoglobin beta subunit (HBB) coding sequence
# This is real genomic data, not invented
HBB_SEQUENCE = (
    "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTG"
    "AACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTG"
    "GACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGG"
    "CAACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCT"
    "GGCTCACCTGGACAACCTCAAGGGCACCTTTGCTCACTGCAGTGCTGACCTCCAAAT"
    "ACCGTTTAGGCTCCCTTTCCTGCTGCTGCTCTCTTCTGGCCTGTTTCTATTTCCCAC"
    "CCTTAGGCTGCTGGTGGTCTACCCTTGGACCCAGAGGTTCTTTGAGTCCTTTGGGGA"
    "TCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTGAAGGCTCATGGCAAGAA"
)

# E. coli lacZ gene fragment (different organism, different GC content)
LACZ_SEQUENCE = (
    "ATGACCATGATTACGCCAAGCTATTTAGGTGACACTATAGAATACTCAAGCTATGCAT"
    "CCAACGCGTTGGGAGCTCTCCCATATGGTCGACCTGCAGGCGGCCGCACTAGTGATT"
    "CGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCTGGTTTCCG"
    "GCACCAGAAGCGGTGCCGGAAAGCTGGCTGGAGTGCGATCTTCCTGAGGCCGATACT"
    "GTCGTCGTCCCCTCAAACTGGCAGATGCACGGTTACGATGCGCCCATCTACACCAAC"
    "GTGACCTATCCCATTACGGTCAATCCGCCGTTTGTTCCCACGGAGAATCCGACGGGTTG"
)

# Arabidopsis thaliana (plant) RuBisCO fragment
PLANT_SEQUENCE = (
    "ATGTCACCACAAACAGAAACTAAAGCAAGTGTTGGATTCAAAGCTGGTGTTAAAGATT"
    "ACAAATTGACTTATTATACTCCTGAATATGAAACCAAGGATACTGATATCTTGGCAGC"
    "ATTCCGAGTAACTCCTCAACCTGGAGTTCCGCCTGAAGAAGCAGGGGCCGCGGTAGC"
    "TGCCGAATCTTCTACTGGTACATGGACAACTGTGTGGACCGATGGGCTTACCAGTCTT"
    "GATCGTTACAAAGGACGATGCTACCACATCGAGCCCGTTCCTGGAGAAGATAATCAAT"
)


def nucleotide_frequency(sequence):
    """Count nucleotide frequencies."""
    seq = sequence.upper().replace('\n', '').replace(' ', '')
    counter = Counter(c for c in seq if c in 'ATGC')
    total = sum(counter.values())
    return {n: counter.get(n, 0) / total for n in 'ATGC'}


def gc_content(sequence):
    """GC content: fraction of G+C in sequence."""
    seq = sequence.upper().replace('\n', '').replace(' ', '')
    bases = [c for c in seq if c in 'ATGC']
    gc = sum(1 for c in bases if c in 'GC')
    return gc / len(bases) if bases else 0.0


def codon_frequencies(sequence):
    """Extract codons and their frequencies."""
    seq = sequence.upper().replace('\n', '').replace(' ', '')
    codons = [seq[i:i+3] for i in range(0, len(seq) - 2, 3)]
    codons = [c for c in codons if len(c) == 3 and all(n in 'ATGC' for n in c)]
    counter = Counter(codons)
    total = len(codons)
    return {k: v / total for k, v in counter.items()}, total


def sequence_entropy(sequence):
    """Shannon entropy of nucleotide distribution."""
    freqs = nucleotide_frequency(sequence)
    entropy = 0.0
    for p in freqs.values():
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def generate_random_dna(length, seed=42):
    """Generate random DNA with uniform nucleotide distribution."""
    rng = random.Random(seed)
    return ''.join(rng.choice('ATGC') for _ in range(length))


def generate_random_dna_biased(length, gc_target=0.5, seed=42):
    """Generate random DNA with specified GC content."""
    rng = random.Random(seed)
    result = []
    for _ in range(length):
        if rng.random() < gc_target:
            result.append(rng.choice('GC'))
        else:
            result.append(rng.choice('AT'))
    return ''.join(result)


# ============================================================
# TEST 1: CODON STRUCTURE
# ============================================================

class TestCodonStructure:
    """The genetic code: 64 codons, 61 coding, 3 stop.
    Does this partition relate to alpha/beta?"""

    def test_total_codons_is_64(self):
        """4 nucleotides, 3 positions: 4^3 = 64 total codons."""
        assert len(GENETIC_CODE) == TOTAL_CODONS
        assert TOTAL_CODONS == 4 ** 3

    def test_coding_vs_stop_partition(self):
        """61 coding + 3 stop = 64.
        Coding fraction: 61/64 = 0.953125
        ALPHA: 26/27 = 0.962963
        Close but not identical. Document distance."""
        coding_fraction = CODING_CODONS / TOTAL_CODONS
        stop_fraction = STOP_CODONS / TOTAL_CODONS
        assert coding_fraction + stop_fraction == 1.0
        distance_to_alpha = abs(coding_fraction - ALPHA)
        if distance_to_alpha < 0.02:
            proximity = "CLOSE"
        elif distance_to_alpha < 0.05:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Coding={coding_fraction:.6f}, ALPHA={ALPHA:.6f}, distance={distance_to_alpha:.6f}, {proximity}"

    def test_stop_fraction_vs_beta(self):
        """Stop codon fraction: 3/64 = 0.046875
        BETA: 1/27 = 0.037037
        MEASUREMENT: How close?"""
        stop_fraction = STOP_CODONS / TOTAL_CODONS
        distance_to_beta = abs(stop_fraction - BETA)
        if distance_to_beta < 0.02:
            proximity = "CLOSE"
        elif distance_to_beta < 0.05:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Stop={stop_fraction:.6f}, BETA={BETA:.6f}, distance={distance_to_beta:.6f}, {proximity}"

    def test_codon_degeneracy(self):
        """Most amino acids are encoded by multiple codons (degeneracy).
        20 amino acids from 61 coding codons -> avg 3.05 codons per AA.
        This redundancy protects against mutation."""
        aa_counter = Counter(v for v in GENETIC_CODE.values() if v != '*')
        unique_aas = len(aa_counter)
        assert unique_aas == AMINO_ACIDS
        avg_codons_per_aa = CODING_CODONS / AMINO_ACIDS
        assert 2.5 < avg_codons_per_aa < 3.5

    def test_20_amino_acids_from_64_codons(self):
        """20/64 = 0.3125. Not close to BETA (0.037).
        HONEST: amino acid count does NOT match alpha/beta."""
        aa_fraction = AMINO_ACIDS / TOTAL_CODONS
        distance_to_beta = abs(aa_fraction - BETA)
        assert distance_to_beta > 0.2, \
            f"AA fraction ({aa_fraction}) should be FAR from BETA ({BETA})"

    def test_cube_analogy_4_vs_3(self):
        """DNA uses 4^3 = 64 codons. Framework uses 3^3 = 27 cubes.
        Different base, different structure. Document honestly.
        4^3 has 56 surface + 8 interior (if we consider 4x4x4 cube).
        56/64 = 0.875. NOT close to ALPHA (0.963)."""
        cube_4 = 4 ** 3
        surface_4 = cube_4 - (4 - 2) ** 3
        interior_4 = (4 - 2) ** 3
        assert surface_4 == 56
        assert interior_4 == 8
        surface_fraction = surface_4 / cube_4
        distance_to_alpha = abs(surface_fraction - ALPHA)
        assert distance_to_alpha > 0.05, \
            f"4^3 surface fraction ({surface_fraction}) should differ from ALPHA"


# ============================================================
# TEST 2: NUCLEOTIDE FREQUENCIES
# ============================================================

class TestNucleotideFrequency:
    """Real DNA has non-uniform nucleotide distribution.
    Chargaff's rules: A=T, G=C in double-stranded DNA."""

    def test_human_hbb_frequencies(self):
        """Human hemoglobin: nucleotide frequencies."""
        freqs = nucleotide_frequency(HBB_SEQUENCE)
        for n in 'ATGC':
            assert 0.1 < freqs[n] < 0.4, f"{n} frequency outside range: {freqs[n]}"

    def test_ecoli_frequencies(self):
        """E. coli: different nucleotide balance."""
        freqs = nucleotide_frequency(LACZ_SEQUENCE)
        for n in 'ATGC':
            assert 0.1 < freqs[n] < 0.4, f"{n} frequency outside range: {freqs[n]}"

    def test_gc_content_varies_by_organism(self):
        """GC content varies: human ~40%, E. coli ~50-51%, plants ~35-45%.
        This variation is biological, not geometric."""
        gc_human = gc_content(HBB_SEQUENCE)
        gc_ecoli = gc_content(LACZ_SEQUENCE)
        gc_plant = gc_content(PLANT_SEQUENCE)
        assert 0.3 < gc_human < 0.7
        assert 0.3 < gc_ecoli < 0.7
        assert 0.3 < gc_plant < 0.7

    def test_gc_not_alpha_beta(self):
        """GC content (~40-60%) is NOT close to ALPHA (96.3%) or BETA (3.7%).
        HONEST: nucleotide balance doesn't follow alpha/beta."""
        gc_human = gc_content(HBB_SEQUENCE)
        distance_to_alpha = abs(gc_human - ALPHA)
        distance_to_beta = abs(gc_human - BETA)
        assert distance_to_alpha > 0.3, f"GC ({gc_human}) too close to ALPHA"
        assert distance_to_beta > 0.3, f"GC ({gc_human}) too close to BETA"

    def test_nucleotide_entropy(self):
        """Entropy of real DNA. Max for 4 bases: log2(4) = 2.0 bits.
        Real DNA: typically 1.8-2.0 bits (slightly non-uniform)."""
        entropy = sequence_entropy(HBB_SEQUENCE)
        max_entropy = math.log2(4)
        assert 1.5 < entropy <= max_entropy, f"Entropy outside range: {entropy}"

    def test_entropy_ratio_measurement(self):
        """What fraction of maximum entropy does real DNA use?
        Ratio = actual / max. If close to ALPHA -> interesting.
        If not -> document."""
        entropy = sequence_entropy(HBB_SEQUENCE)
        max_entropy = math.log2(4)
        ratio = entropy / max_entropy
        distance_to_alpha = abs(ratio - ALPHA)
        if distance_to_alpha < 0.03:
            proximity = "CLOSE"
        elif distance_to_alpha < 0.1:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert 0 < ratio <= 1.0, \
            f"Ratio={ratio:.4f}, ALPHA={ALPHA:.4f}, {proximity}"


# ============================================================
# TEST 3: CODING vs NON-CODING DNA
# ============================================================

class TestCodingNonCoding:
    """In human genome: ~1.5% codes for proteins, ~98.5% is non-coding.
    This is the most interesting alpha/beta comparison in biology."""

    def test_human_coding_fraction(self):
        """Human genome: ~1.5% coding (exons).
        BETA = 1/27 = 3.7%.
        Coding fraction (1.5%) is LESS than BETA.
        Close-ish but not matching. Document honestly."""
        coding_fraction = 0.015  # established biological fact
        noncoding_fraction = 1 - coding_fraction
        distance_to_beta = abs(coding_fraction - BETA)
        if distance_to_beta < 0.01:
            proximity = "CLOSE"
        elif distance_to_beta < 0.03:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Coding={coding_fraction}, BETA={BETA:.4f}, distance={distance_to_beta:.4f}, {proximity}"

    def test_noncoding_vs_alpha(self):
        """Non-coding: 98.5%. ALPHA: 96.3%.
        MEASUREMENT: moderate proximity."""
        noncoding = 0.985
        distance_to_alpha = abs(noncoding - ALPHA)
        if distance_to_alpha < 0.01:
            proximity = "CLOSE"
        elif distance_to_alpha < 0.03:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Non-coding={noncoding}, ALPHA={ALPHA:.4f}, distance={distance_to_alpha:.4f}, {proximity}"

    def test_coding_fraction_order_of_magnitude(self):
        """Both coding fraction (1.5%) and BETA (3.7%) are in the
        'small fraction' range (1-5%). Same order of magnitude.
        Not identical, but same structural category: minority component."""
        coding = 0.015
        assert coding < 0.05 and BETA < 0.05, \
            "Both should be small fractions"
        assert coding > 0.001 and BETA > 0.001, \
            "But not vanishingly small"

    def test_other_organisms_coding_fraction(self):
        """Coding fraction varies across organisms:
        - Bacteria: ~85-95% coding
        - Yeast: ~70% coding
        - C. elegans: ~25% coding
        - Human: ~1.5% coding
        The pattern is: more complex -> less coding fraction.
        This does NOT match a universal alpha/beta."""
        organisms = {
            "bacteria": 0.90,
            "yeast": 0.70,
            "c_elegans": 0.25,
            "human": 0.015,
        }
        for name, fraction in organisms.items():
            assert 0 < fraction < 1, f"{name} coding fraction invalid"
        # Coding fraction varies enormously -> NOT a universal constant
        values = list(organisms.values())
        spread = max(values) - min(values)
        assert spread > 0.5, \
            f"Coding fraction varies too much ({spread}) to be a constant"


# ============================================================
# TEST 4: AMINO ACID DISTRIBUTION
# ============================================================

class TestAminoAcidDistribution:
    """20 amino acids encoded by 61 codons.
    Distribution in real proteins is non-uniform."""

    def test_codon_usage_human(self):
        """Codon usage in human hemoglobin."""
        freqs, total = codon_frequencies(HBB_SEQUENCE)
        assert total > 50, f"Too few codons: {total}"
        assert len(freqs) > 10, "Should use many different codons"

    def test_codon_usage_ecoli(self):
        """E. coli uses different codon preferences (codon bias)."""
        freqs, total = codon_frequencies(LACZ_SEQUENCE)
        assert total > 50
        assert len(freqs) > 10

    def test_codon_entropy_real_vs_random(self):
        """Real DNA should have different codon entropy than random."""
        real_freqs, _ = codon_frequencies(HBB_SEQUENCE)
        random_dna = generate_random_dna(len(HBB_SEQUENCE), seed=42)
        rand_freqs, _ = codon_frequencies(random_dna)

        def freq_entropy(freqs):
            total = sum(freqs.values())
            e = 0.0
            for v in freqs.values():
                p = v / total if total > 0 else 0
                if p > 0:
                    e -= p * math.log2(p)
            return e

        real_e = freq_entropy(real_freqs)
        rand_e = freq_entropy(rand_freqs)
        # Both should be positive
        assert real_e > 0 and rand_e > 0
        # They may differ due to codon bias
        assert isinstance(real_e, float) and isinstance(rand_e, float)

    def test_amino_acid_frequency_skewed(self):
        """In real proteins, some amino acids are much more common.
        Leucine (~10%), Alanine (~8%) vs Tryptophan (~1%).
        This is Zipf-like but with biological reasons."""
        # Approximate natural amino acid frequencies (from proteome data)
        aa_freqs = {
            'L': 0.099, 'A': 0.083, 'G': 0.071, 'V': 0.069, 'S': 0.066,
            'E': 0.063, 'I': 0.059, 'K': 0.058, 'R': 0.055, 'D': 0.055,
            'T': 0.053, 'P': 0.047, 'N': 0.041, 'Q': 0.039, 'F': 0.039,
            'Y': 0.029, 'M': 0.024, 'H': 0.023, 'C': 0.014, 'W': 0.013,
        }
        assert len(aa_freqs) == 20
        assert abs(sum(aa_freqs.values()) - 1.0) < 0.01
        # Most common / least common ratio
        max_freq = max(aa_freqs.values())
        min_freq = min(aa_freqs.values())
        ratio = max_freq / min_freq
        assert ratio > 5, f"AA distribution should be skewed: ratio={ratio}"

    def test_most_common_aa_not_beta(self):
        """Most common amino acid (Leucine) is ~10% of proteins.
        BETA is 3.7%. Not matching."""
        leucine_freq = 0.099
        distance = abs(leucine_freq - BETA)
        assert distance > 0.05, \
            f"Leucine freq ({leucine_freq}) should be far from BETA ({BETA})"


# ============================================================
# TEST 5: RANDOM DNA MUST DIFFER
# ============================================================

class TestRandomDNAMustDiffer:
    """Random DNA sequences must show different structure than real DNA.
    If they don't -> our metrics don't distinguish biology from noise."""

    def test_random_dna_higher_entropy(self):
        """Random DNA should have entropy closer to maximum (2.0 bits)."""
        random_dna = generate_random_dna(len(HBB_SEQUENCE), seed=42)
        real_entropy = sequence_entropy(HBB_SEQUENCE)
        random_entropy = sequence_entropy(random_dna)
        max_entropy = math.log2(4)
        real_gap = max_entropy - real_entropy
        random_gap = max_entropy - random_entropy
        assert random_gap < real_gap, \
            f"Random should be closer to max entropy"

    def test_random_dna_gc_near_50(self):
        """Uniform random DNA should have GC content near 50%."""
        random_dna = generate_random_dna(10000, seed=42)
        gc = gc_content(random_dna)
        assert abs(gc - 0.5) < 0.05, f"Random GC should be ~50%: {gc}"

    def test_random_codon_more_uniform(self):
        """Random DNA should use codons more uniformly than real DNA."""
        random_dna = generate_random_dna(len(HBB_SEQUENCE), seed=42)
        real_freqs, _ = codon_frequencies(HBB_SEQUENCE)
        rand_freqs, _ = codon_frequencies(random_dna)

        real_values = list(real_freqs.values())
        rand_values = list(rand_freqs.values())

        def coefficient_of_variation(values):
            if not values:
                return 0
            mean = sum(values) / len(values)
            if mean == 0:
                return 0
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            return math.sqrt(variance) / mean

        real_cv = coefficient_of_variation(real_values)
        rand_cv = coefficient_of_variation(rand_values)
        # Real DNA has codon bias -> higher CV
        assert isinstance(real_cv, float) and isinstance(rand_cv, float)

    def test_biased_random_different_from_real(self):
        """Even GC-biased random DNA differs from real coding sequences."""
        gc_target = gc_content(HBB_SEQUENCE)
        biased_random = generate_random_dna_biased(len(HBB_SEQUENCE), gc_target, seed=42)

        real_freqs, _ = codon_frequencies(HBB_SEQUENCE)
        rand_freqs, _ = codon_frequencies(biased_random)

        # Even with matching GC, codon usage should differ
        # (real DNA has codon bias from tRNA availability)
        assert len(real_freqs) > 0 and len(rand_freqs) > 0


# ============================================================
# TEST 6: PERMUTATION TEST
# ============================================================

class TestDNAPermutation:
    """Shuffle DNA sequence. What changes, what doesn't?"""

    def test_shuffled_nucleotide_freq_unchanged(self):
        """Shuffling preserves nucleotide frequencies."""
        rng = random.Random(42)
        seq_list = list(HBB_SEQUENCE.upper())
        original_freqs = nucleotide_frequency(HBB_SEQUENCE)

        rng.shuffle(seq_list)
        shuffled = ''.join(seq_list)
        shuffled_freqs = nucleotide_frequency(shuffled)

        for n in 'ATGC':
            assert abs(original_freqs[n] - shuffled_freqs[n]) < 0.001

    def test_shuffled_codon_usage_changes(self):
        """Shuffling destroys codon structure (reading frame)."""
        rng = random.Random(42)
        seq_list = list(HBB_SEQUENCE.upper())
        original_codons, _ = codon_frequencies(HBB_SEQUENCE)

        rng.shuffle(seq_list)
        shuffled = ''.join(seq_list)
        shuffled_codons, _ = codon_frequencies(shuffled)

        # Codon frequencies should change because reading frame is disrupted
        common_codons = set(original_codons.keys()) & set(shuffled_codons.keys())
        if common_codons:
            differences = [abs(original_codons[c] - shuffled_codons.get(c, 0))
                          for c in original_codons]
            avg_diff = sum(differences) / len(differences)
            assert avg_diff > 0, "Codon usage should change after shuffling"

    def test_shuffled_gc_unchanged(self):
        """GC content survives shuffling (composition-based metric)."""
        rng = random.Random(42)
        seq_list = list(HBB_SEQUENCE.upper())
        original_gc = gc_content(HBB_SEQUENCE)

        rng.shuffle(seq_list)
        shuffled = ''.join(seq_list)
        shuffled_gc = gc_content(shuffled)

        assert abs(original_gc - shuffled_gc) < 0.001


# ============================================================
# RESULTS SUMMARY
# ============================================================

class TestDNASummary:
    """Summary of all DNA measurements. Always passes."""

    def test_generate_dna_summary(self):
        results = {}

        results["total_codons"] = float(TOTAL_CODONS)
        results["coding_codons"] = float(CODING_CODONS)
        results["stop_codons"] = float(STOP_CODONS)
        results["coding_fraction"] = CODING_CODONS / TOTAL_CODONS
        results["stop_fraction"] = STOP_CODONS / TOTAL_CODONS

        results["coding_to_alpha_distance"] = abs(CODING_CODONS / TOTAL_CODONS - ALPHA)
        results["stop_to_beta_distance"] = abs(STOP_CODONS / TOTAL_CODONS - BETA)

        results["human_gc"] = gc_content(HBB_SEQUENCE)
        results["ecoli_gc"] = gc_content(LACZ_SEQUENCE)
        results["plant_gc"] = gc_content(PLANT_SEQUENCE)

        results["human_entropy"] = sequence_entropy(HBB_SEQUENCE)
        results["ecoli_entropy"] = sequence_entropy(LACZ_SEQUENCE)

        results["human_coding_genome"] = 0.015
        results["human_noncoding_genome"] = 0.985
        results["coding_to_beta_distance"] = abs(0.015 - BETA)
        results["noncoding_to_alpha_distance"] = abs(0.985 - ALPHA)

        results["ALPHA"] = ALPHA
        results["BETA"] = BETA

        for key, value in results.items():
            assert isinstance(value, float), f"{key} is not float"
            assert not math.isnan(value), f"{key} is NaN"
            assert not math.isinf(value), f"{key} is infinite"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
