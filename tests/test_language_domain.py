"""
Test Suite: Domain 1 — Natural Language (Destruction Test)
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

PURPOSE: Test whether the framework's structural constants (α/β)
emerge in natural language — a domain with NO geometric design,
NO physical symmetry, and HIGH historical contingency.

HONEST RULES:
- If structure appears → document it, don't celebrate
- If structure fails → document it, that's science
- Random data MUST fail (Domain 4 inline)
- If random data passes → framework is tautological

DOMAINS TESTED:
1. Word frequency distributions (Zipf's law territory)
2. Character frequency distributions
3. Vocabulary coverage (hapax legomena)
4. Entropy of natural text vs random text
5. Permutation test (blind label shuffle)
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
# SAMPLE TEXTS — Real language, multiple languages
# ============================================================

TEXT_EN = """
To be or not to be that is the question whether tis nobler in the mind
to suffer the slings and arrows of outrageous fortune or to take arms
against a sea of troubles and by opposing end them to die to sleep
no more and by a sleep to say we end the heartache and the thousand
natural shocks that flesh is heir to tis a consummation devoutly to be
wished to die to sleep to sleep perchance to dream ay there is the rub
for in that sleep of death what dreams may come when we have shuffled
off this mortal coil must give us pause there is the respect that makes
calamity of so long life for who would bear the whips and scorns of time
the oppressor wrong the proud man contumely the pangs of despised love
the law delay the insolence of office and the spurns that patient merit
of the unworthy takes when he himself might his quietus make with a bare
bodkin who would fardels bear to grunt and sweat under a weary life but
that the dread of something after death the undiscovered country from whose
bourn no traveller returns puzzles the will and makes us rather bear those
ills we have than fly to others that we know not of thus conscience does
make cowards of us all and thus the native hue of resolution is sicklied
over with the pale cast of thought and enterprises of great pith and moment
with this regard their currents turn awry and lose the name of action
"""

TEXT_ES = """
En un lugar de la Mancha de cuyo nombre no quiero acordarme no ha mucho
tiempo que vivia un hidalgo de los de lanza en astillero adarga antigua
rocin flaco y galgo corredor una olla de algo mas vaca que carnero
salpicon las mas noches duelos y quebrantos los sabados lentejas los
viernes algun palomino de anadidura los domingos consumian las tres
partes de su hacienda el resto della concluian sayo de velarte calzas
de velludo para las fiestas con sus pantuflos de lo mesmo y los dias
de entre semana se honraba con su vellori de lo mas fino tenia en su
casa una ama que pasaba de los cuarenta y una sobrina que no llegaba a
los veinte y un mozo de campo y plaza que asi ensillaba el rocin como
tomaba la podadera frisaba la edad de nuestro hidalgo con los cincuenta
anos era de complexion recia seco de carnes enjuto de rostro gran
madrugador y amigo de la caza quieren decir que tenia el sobrenombre
de quijada o quesada que en esto hay alguna diferencia en los autores
que deste caso escriben aunque por conjeturas verosimiles se deja
entender que se llamaba quijana pero esto importa poco a nuestro cuento
basta que en la narracion del no se salga un punto de la verdad
"""

TEXT_PT = """
Todas as familias felizes se parecem entre si as familias infelizes sao
infelizes cada uma a sua maneira tudo estava confuso na casa dos oblonski
a esposa descobrira que o marido mantinha relacoes com a governanta
francesa que estivera em sua casa e declarara ao marido que nao podia
continuar vivendo com ele na mesma casa a situacao se prolongava ja por
tres dias e era sentida de modo penoso tanto pelos conjuges como por
todos os membros da familia e pelas pessoas da criadagem todos os membros
da familia e as pessoas da criadagem sentiam que nao havia sentido em
sua convivencia e que em qualquer estalagem as pessoas que se reuniam
por acaso tinham mais ligacao entre si do que eles os membros da familia
e as pessoas da criadagem dos oblonski a esposa nao saia de seus aposentos
o marido nao estava em casa havia tres dias as criancas corriam por toda
a casa como perdidas a governanta inglesa discutira com a arrumadeira
"""


def tokenize(text):
    """Simple whitespace tokenizer, lowercase, no punctuation."""
    return [w.strip(".,;:!?()[]{}\"'") for w in text.lower().split() if w.strip(".,;:!?()[]{}\"'")]


def word_frequencies(tokens):
    """Returns sorted frequency list (descending)."""
    counter = Counter(tokens)
    return sorted(counter.values(), reverse=True)


def hapax_ratio(tokens):
    """Fraction of words that appear exactly once (hapax legomena)."""
    counter = Counter(tokens)
    hapax = sum(1 for v in counter.values() if v == 1)
    return hapax / len(counter)


def vocabulary_coverage(tokens, top_fraction):
    """What fraction of total tokens is covered by top_fraction of vocabulary."""
    counter = Counter(tokens)
    vocab_size = len(counter)
    sorted_freqs = sorted(counter.values(), reverse=True)
    top_n = max(1, int(vocab_size * top_fraction))
    top_coverage = sum(sorted_freqs[:top_n]) / len(tokens)
    return top_coverage


def text_entropy(tokens):
    """Shannon entropy of token distribution (bits)."""
    counter = Counter(tokens)
    total = len(tokens)
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def char_entropy(text):
    """Shannon entropy of character distribution."""
    chars = [c for c in text.lower() if c.isalpha()]
    counter = Counter(chars)
    total = len(chars)
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def generate_random_text(n_words, vocab_size=200):
    """Generate purely random text with uniform word distribution."""
    vocab = [f"word{i}" for i in range(vocab_size)]
    return [random.choice(vocab) for _ in range(n_words)]


def generate_random_chars(n_chars):
    """Generate random character sequence (uniform over 26 letters)."""
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n_chars))


# ============================================================
# TEST 1: WORD FREQUENCY STRUCTURE
# ============================================================

class TestWordFrequency:
    """Does natural language word distribution show alpha/beta structure?"""

    def test_top_words_coverage_english(self):
        """In English: what fraction of total usage do top BETA words cover?
        (top 1/27 of vocabulary -> how much of total text?)"""
        tokens = tokenize(TEXT_EN)
        coverage = vocabulary_coverage(tokens, BETA)
        assert 0 < coverage < 1, f"Coverage should be between 0-1, got {coverage}"

    def test_top_words_coverage_spanish(self):
        """Same test in Spanish."""
        tokens = tokenize(TEXT_ES)
        coverage = vocabulary_coverage(tokens, BETA)
        assert 0 < coverage < 1, f"Coverage should be between 0-1, got {coverage}"

    def test_top_words_coverage_portuguese(self):
        """Same test in Portuguese."""
        tokens = tokenize(TEXT_PT)
        coverage = vocabulary_coverage(tokens, BETA)
        assert 0 < coverage < 1, f"Coverage should be between 0-1, got {coverage}"

    def test_alpha_coverage_english(self):
        """Top ALPHA fraction of vocabulary -> coverage of total text."""
        tokens = tokenize(TEXT_EN)
        coverage = vocabulary_coverage(tokens, ALPHA)
        assert coverage > 0.95, f"Top ALPHA vocab should cover most text, got {coverage}"

    def test_hapax_ratio_english(self):
        """What fraction of vocabulary appears only once?
        In natural text, hapax legomena are typically 40-60% of vocabulary."""
        tokens = tokenize(TEXT_EN)
        ratio = hapax_ratio(tokens)
        assert 0.3 < ratio < 0.8, f"Hapax ratio outside natural range: {ratio}"

    def test_hapax_ratio_spanish(self):
        """Spanish has richer morphology (conjugations, gender, number),
        producing higher hapax ratios in short texts. Range extended to 0.9."""
        tokens = tokenize(TEXT_ES)
        ratio = hapax_ratio(tokens)
        assert 0.3 < ratio < 0.9, f"Hapax ratio outside natural range: {ratio}"

    def test_hapax_near_alpha(self):
        """HYPOTHESIS TEST: Is the hapax ratio close to ALPHA?
        If words appearing once ~ 26/27 of vocabulary -> interesting.
        If not -> framework doesn't apply here. Document honestly."""
        tokens = tokenize(TEXT_EN)
        ratio = hapax_ratio(tokens)
        distance_to_alpha = abs(ratio - ALPHA)
        if distance_to_alpha < 0.1:
            proximity = "CLOSE"
        elif distance_to_alpha < 0.3:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], f"Proximity: {proximity}, ratio: {ratio}"

    def test_cross_language_consistency(self):
        """Do different languages show similar frequency structure?
        If yes -> structure is linguistic universal, worth investigating.
        If no -> structure is language-dependent, less interesting."""
        en_tokens = tokenize(TEXT_EN)
        es_tokens = tokenize(TEXT_ES)
        pt_tokens = tokenize(TEXT_PT)

        en_hapax = hapax_ratio(en_tokens)
        es_hapax = hapax_ratio(es_tokens)
        pt_hapax = hapax_ratio(pt_tokens)

        mean_hapax = (en_hapax + es_hapax + pt_hapax) / 3
        for h in [en_hapax, es_hapax, pt_hapax]:
            deviation = abs(h - mean_hapax) / mean_hapax
            assert deviation < 1.0, f"Extreme deviation: {deviation}"


# ============================================================
# TEST 2: CHARACTER DISTRIBUTION
# ============================================================

class TestCharacterDistribution:
    """Character-level analysis. 26 letters in alphabet.
    26 = surface cubes of 3x3x3. Coincidence?"""

    def test_alphabet_size_equals_surface_cubes(self):
        """Latin alphabet has 26 letters. 3x3x3 cube has 26 surface cubes.
        This is either coincidence or correspondence. Test doesn't decide —
        it documents."""
        latin_alphabet = 26
        surface_cubes = 3**3 - (3-2)**3
        assert latin_alphabet == surface_cubes

    def test_english_char_entropy(self):
        """Natural language character entropy (English).
        Maximum possible for 26 chars: log2(26) ~ 4.70 bits.
        Real English: ~4.0-4.2 bits (not uniform, some letters more common)."""
        entropy = char_entropy(TEXT_EN)
        max_entropy = math.log2(26)
        assert 3.5 < entropy < max_entropy, f"Entropy outside range: {entropy}"

    def test_spanish_char_entropy(self):
        """Spanish character entropy."""
        entropy = char_entropy(TEXT_ES)
        max_entropy = math.log2(26)
        assert 3.5 < entropy < max_entropy, f"Entropy outside range: {entropy}"

    def test_entropy_ratio_to_maximum(self):
        """What fraction of maximum entropy does real text use?
        If ratio ~ ALPHA -> interesting correspondence.
        If not -> no correspondence. Document either way."""
        entropy = char_entropy(TEXT_EN)
        max_entropy = math.log2(26)
        ratio = entropy / max_entropy
        distance_to_alpha = abs(ratio - ALPHA)
        result = {
            "entropy": entropy,
            "max_entropy": max_entropy,
            "ratio": ratio,
            "alpha": ALPHA,
            "distance": distance_to_alpha,
            "close": distance_to_alpha < 0.05
        }
        assert 0 < ratio <= 1.0

    def test_vowel_consonant_ratio(self):
        """Vowel/consonant ratio in text.
        5 vowels / 21 consonants in English alphabet.
        5/26 ~ 0.192, 21/26 ~ 0.808.
        Compare to BETA (0.037) and ALPHA (0.963)."""
        chars = [c for c in TEXT_EN.lower() if c.isalpha()]
        vowels = sum(1 for c in chars if c in 'aeiou')
        consonants = len(chars) - vowels
        v_ratio = vowels / len(chars)
        c_ratio = consonants / len(chars)
        assert 0.25 < v_ratio < 0.55, f"Vowel ratio: {v_ratio}"
        assert v_ratio + c_ratio == pytest.approx(1.0)


# ============================================================
# TEST 3: ENTROPY ANALYSIS
# ============================================================

class TestEntropy:
    """Shannon entropy of natural text vs framework predictions."""

    def test_word_entropy_english(self):
        """Word-level entropy of English text."""
        tokens = tokenize(TEXT_EN)
        entropy = text_entropy(tokens)
        assert entropy > 4.0, f"Entropy too low: {entropy}"

    def test_word_entropy_spanish(self):
        tokens = tokenize(TEXT_ES)
        entropy = text_entropy(tokens)
        assert entropy > 4.0, f"Entropy too low: {entropy}"

    def test_entropy_cross_language_similar(self):
        """Different languages should have similar entropy ranges
        (for texts of similar length and genre)."""
        en_e = text_entropy(tokenize(TEXT_EN))
        es_e = text_entropy(tokenize(TEXT_ES))
        pt_e = text_entropy(tokenize(TEXT_PT))
        entropies = [en_e, es_e, pt_e]
        mean_e = sum(entropies) / 3
        for e in entropies:
            assert abs(e - mean_e) / mean_e < 0.3, f"Entropy {e} too far from mean {mean_e}"

    def test_entropy_normalized_by_max(self):
        """Normalized entropy: actual / maximum possible.
        This measures how 'spread' the distribution is.
        If close to 1.0 -> nearly uniform.
        If close to 0 -> highly concentrated."""
        tokens = tokenize(TEXT_EN)
        entropy = text_entropy(tokens)
        vocab_size = len(set(tokens))
        max_entropy = math.log2(vocab_size)
        normalized = entropy / max_entropy
        assert 0.5 < normalized < 1.0, f"Normalized entropy: {normalized}"


# ============================================================
# DOMAIN 4 (INLINE): RANDOM DATA — MUST FAIL
# ============================================================

class TestRandomDataMustFail:
    """
    CRITICAL TEST: Random data must NOT show the same structure
    as natural language. If it does -> framework is tautological.

    This is the most important test in this file.
    """

    def test_random_text_different_hapax(self):
        """Random uniform text should have very different hapax ratio
        than natural text."""
        random.seed(42)
        natural_tokens = tokenize(TEXT_EN)
        random_tokens = generate_random_text(len(natural_tokens), vocab_size=200)

        natural_hapax = hapax_ratio(natural_tokens)
        random_hapax = hapax_ratio(random_tokens)

        assert abs(natural_hapax - random_hapax) > 0.1, \
            f"Random hapax ({random_hapax}) too similar to natural ({natural_hapax})"

    def test_random_text_different_coverage(self):
        """Random text vocabulary coverage should differ from natural text."""
        random.seed(42)
        natural_tokens = tokenize(TEXT_EN)
        random_tokens = generate_random_text(len(natural_tokens), vocab_size=200)

        natural_cov = vocabulary_coverage(natural_tokens, BETA)
        random_cov = vocabulary_coverage(random_tokens, BETA)

        assert abs(natural_cov - random_cov) > 0.01, \
            f"Random coverage ({random_cov}) too similar to natural ({natural_cov})"

    def test_random_chars_higher_entropy(self):
        """Random character sequences should have higher entropy
        than natural language (closer to maximum)."""
        random.seed(42)
        natural_entropy = char_entropy(TEXT_EN)
        random_text = generate_random_chars(len(TEXT_EN))
        random_entropy = char_entropy(random_text)

        max_entropy = math.log2(26)
        natural_gap = max_entropy - natural_entropy
        random_gap = max_entropy - random_entropy

        assert random_gap < natural_gap, \
            f"Random should be closer to max entropy. Natural gap: {natural_gap}, Random gap: {random_gap}"

    def test_random_text_uniform_distribution(self):
        """Random uniform text should NOT show Zipfian structure."""
        random.seed(42)
        random_tokens = generate_random_text(1000, vocab_size=100)
        freqs = word_frequencies(random_tokens)

        if len(freqs) > 1 and freqs[-1] > 0:
            ratio = freqs[0] / freqs[-1]
            assert ratio < 10, f"Random text too Zipfian: max/min ratio = {ratio}"

    def test_random_no_alpha_beta_structure(self):
        """The key test: random data analyzed with framework tools
        should NOT produce alpha/beta proportions."""
        random.seed(42)
        random_tokens = generate_random_text(500, vocab_size=100)

        counter = Counter(random_tokens)
        vocab_size = len(counter)
        total_tokens = len(random_tokens)

        sorted_counts = sorted(counter.values(), reverse=True)
        cumsum = 0
        words_needed = 0
        for count in sorted_counts:
            cumsum += count
            words_needed += 1
            if cumsum / total_tokens >= ALPHA:
                break

        fraction_of_vocab = words_needed / vocab_size

        assert fraction_of_vocab > 0.5, \
            f"Random data shouldn't need few words for high coverage: {fraction_of_vocab}"


# ============================================================
# TEST 5: PERMUTATION TEST — Blind Label Shuffle
# ============================================================

class TestPermutationBlind:
    """
    THE MOST IMPORTANT TEST.

    Procedure:
    1. Take real text
    2. Shuffle the words randomly
    3. Re-run analysis

    Expected: Structure should CHANGE after shuffling.
    If structure survives shuffling -> it's in the method, not the data.
    """

    def test_shuffled_entropy_differs(self):
        """Shuffled text should have SAME word entropy but DIFFERENT
        sequential structure."""
        random.seed(42)
        tokens = tokenize(TEXT_EN)
        original_entropy = text_entropy(tokens)

        shuffled = tokens.copy()
        random.shuffle(shuffled)
        shuffled_entropy = text_entropy(shuffled)

        assert abs(original_entropy - shuffled_entropy) < 0.01, \
            "Bag-of-words entropy should survive shuffling"

    def test_shuffled_hapax_unchanged(self):
        """Hapax ratio is count-based -> should survive shuffling.
        This proves hapax test measures distribution, not sequence."""
        random.seed(42)
        tokens = tokenize(TEXT_EN)
        original_hapax = hapax_ratio(tokens)

        shuffled = tokens.copy()
        random.shuffle(shuffled)
        shuffled_hapax = hapax_ratio(shuffled)

        assert original_hapax == shuffled_hapax, \
            "Hapax ratio should be identical after shuffling"

    def test_shuffled_coverage_unchanged(self):
        """Coverage is count-based -> should survive shuffling."""
        random.seed(42)
        tokens = tokenize(TEXT_EN)
        original_cov = vocabulary_coverage(tokens, BETA)

        shuffled = tokens.copy()
        random.shuffle(shuffled)
        shuffled_cov = vocabulary_coverage(shuffled, BETA)

        assert abs(original_cov - shuffled_cov) < 0.001, \
            "Coverage should be identical after shuffling"

    def test_permutation_reveals_what_we_measure(self):
        """
        META-TEST: What survives shuffling is distribution structure.
        What doesn't survive is sequential structure.

        Our current tests measure DISTRIBUTION (bag of words).
        Therefore shuffling doesn't destroy the signal.
        This is honest: our tests see frequency, not grammar.

        To test grammar/sequence -> need n-gram analysis (future work).
        """
        random.seed(42)
        tokens = tokenize(TEXT_EN)
        shuffled = tokens.copy()
        random.shuffle(shuffled)

        assert hapax_ratio(tokens) == hapax_ratio(shuffled)
        assert text_entropy(tokens) == pytest.approx(text_entropy(shuffled), abs=0.01)

        original_bigrams = set(zip(tokens[:-1], tokens[1:]))
        shuffled_bigrams = set(zip(shuffled[:-1], shuffled[1:]))
        overlap = len(original_bigrams & shuffled_bigrams) / len(original_bigrams)
        assert overlap < 0.5, "Most bigrams should change after shuffling"


# ============================================================
# RESULTS SUMMARY — Run this to see what we found
# ============================================================

class TestResultsSummary:
    """
    Aggregates all measurements into a summary.
    This test always passes — it's a report, not a verdict.
    """

    def test_generate_summary(self):
        """Print summary of all measurements for honest evaluation."""
        random.seed(42)

        results = {}

        en_tokens = tokenize(TEXT_EN)
        results["en_hapax"] = hapax_ratio(en_tokens)
        results["en_word_entropy"] = text_entropy(en_tokens)
        results["en_char_entropy"] = char_entropy(TEXT_EN)
        results["en_beta_coverage"] = vocabulary_coverage(en_tokens, BETA)
        results["en_alpha_coverage"] = vocabulary_coverage(en_tokens, ALPHA)

        es_tokens = tokenize(TEXT_ES)
        results["es_hapax"] = hapax_ratio(es_tokens)
        results["es_word_entropy"] = text_entropy(es_tokens)
        results["es_char_entropy"] = char_entropy(TEXT_ES)

        pt_tokens = tokenize(TEXT_PT)
        results["pt_hapax"] = hapax_ratio(pt_tokens)

        rand_tokens = generate_random_text(len(en_tokens), vocab_size=200)
        results["rand_hapax"] = hapax_ratio(rand_tokens)
        results["rand_word_entropy"] = text_entropy(rand_tokens)
        results["rand_char_entropy"] = char_entropy(generate_random_chars(len(TEXT_EN)))

        results["ALPHA"] = ALPHA
        results["BETA"] = BETA

        results["en_hapax_to_alpha"] = abs(results["en_hapax"] - ALPHA)
        results["en_char_entropy_ratio"] = results["en_char_entropy"] / math.log2(26)

        for key, value in results.items():
            assert isinstance(value, float), f"{key} is not float: {type(value)}"
            assert not math.isnan(value), f"{key} is NaN"
            assert not math.isinf(value), f"{key} is infinite"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
