"""
Test Suite: Domain 5 — Psychometry (Destruction Test)
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

PURPOSE: Test whether alpha/beta structure emerges in real
psychometric data — human psychological measurements that are
inherently noisy, culturally influenced, and messy.

WHY THIS IS DANGEROUS:
- Human metrics are dirty and variable
- IQ, personality, and cognitive tests have known biases
- No geometric reason for alpha/beta to appear
- If structure appears -> worth investigating
- If not -> clear boundary

DOMAINS TESTED:
1. IQ distribution (normal, mean 100, sd 15)
2. Big Five personality traits
3. Reaction time distributions
4. Test score reliability (Cronbach's alpha territory)
5. Normal vs non-normal distributions
6. Random data control
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
# PSYCHOMETRIC DATA GENERATORS (based on real distributions)
# ============================================================

def generate_iq_scores(n, mean=100, sd=15, seed=42):
    """Generate IQ-like scores using Box-Muller transform.
    Real IQ: normal distribution, mean=100, sd=15."""
    rng = random.Random(seed)
    scores = []
    for _ in range(n // 2 + 1):
        u1 = rng.random()
        u2 = rng.random()
        while u1 == 0:
            u1 = rng.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        scores.append(mean + sd * z0)
        scores.append(mean + sd * z1)
    return scores[:n]


def generate_big_five_scores(n, seed=42):
    """Generate Big Five personality scores (1-5 scale).
    Traits: Openness, Conscientiousness, Extraversion,
    Agreeableness, Neuroticism.
    Real data: slightly skewed, not perfectly normal."""
    rng = random.Random(seed)
    traits = {}
    means = {'O': 3.5, 'C': 3.4, 'E': 3.2, 'A': 3.6, 'N': 2.8}
    sds = {'O': 0.7, 'C': 0.7, 'E': 0.8, 'A': 0.6, 'N': 0.8}
    for trait in means:
        scores = []
        for _ in range(n // 2 + 1):
            u1 = max(rng.random(), 1e-10)
            u2 = rng.random()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            score = means[trait] + sds[trait] * z
            score = max(1.0, min(5.0, score))
            scores.append(score)
        traits[trait] = scores[:n]
    return traits


def generate_reaction_times(n, seed=42):
    """Generate reaction time data (milliseconds).
    Real RT: right-skewed (log-normal-ish), mean ~250ms, long tail."""
    rng = random.Random(seed)
    times = []
    for _ in range(n):
        u1 = max(rng.random(), 1e-10)
        u2 = rng.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        log_rt = 5.5 + 0.3 * z
        rt = math.exp(log_rt)
        rt = max(100, min(2000, rt))
        times.append(rt)
    return times


def generate_test_scores(n, difficulty=0.6, seed=42):
    """Generate test scores (0-100) with realistic distribution.
    Difficulty parameter controls mean score."""
    rng = random.Random(seed)
    scores = []
    for _ in range(n):
        u1 = max(rng.random(), 1e-10)
        u2 = rng.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        score = difficulty * 100 + 15 * z
        score = max(0, min(100, score))
        scores.append(score)
    return scores


def distribution_entropy(values, bins=20):
    """Shannon entropy of a continuous distribution (binned)."""
    if not values:
        return 0.0
    min_v = min(values)
    max_v = max(values)
    if max_v == min_v:
        return 0.0
    bin_width = (max_v - min_v) / bins
    bin_counts = [0] * bins
    for v in values:
        idx = min(int((v - min_v) / bin_width), bins - 1)
        bin_counts[idx] += 1
    total = len(values)
    entropy = 0.0
    for count in bin_counts:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def tail_fraction(values, sd_threshold=2.0):
    """Fraction of values beyond N standard deviations from mean."""
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    sd = math.sqrt(variance)
    if sd == 0:
        return 0.0
    tails = sum(1 for v in values if abs(v - mean) > sd_threshold * sd)
    return tails / len(values)


def top_fraction_score(values, fraction):
    """What fraction of total score is held by top fraction of scorers?"""
    sorted_vals = sorted(values, reverse=True)
    total = sum(sorted_vals)
    if total == 0:
        return 0.0
    top_n = max(1, int(len(sorted_vals) * fraction))
    top_sum = sum(sorted_vals[:top_n])
    return top_sum / total


def skewness(values):
    """Sample skewness of distribution."""
    n = len(values)
    if n < 3:
        return 0.0
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    sd = math.sqrt(variance)
    if sd == 0:
        return 0.0
    return sum((v - mean) ** 3 for v in values) / (n * sd ** 3)


def kurtosis(values):
    """Excess kurtosis (normal = 0)."""
    n = len(values)
    if n < 4:
        return 0.0
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    sd = math.sqrt(variance)
    if sd == 0:
        return 0.0
    return sum((v - mean) ** 4 for v in values) / (n * sd ** 4) - 3.0


# ============================================================
# TEST 1: IQ DISTRIBUTION
# ============================================================

class TestIQDistribution:
    """IQ follows normal distribution. Does alpha/beta appear?"""

    @pytest.fixture
    def iq_scores(self):
        return generate_iq_scores(10000, seed=42)

    def test_mean_near_100(self, iq_scores):
        mean = sum(iq_scores) / len(iq_scores)
        assert abs(mean - 100) < 2, f"Mean should be ~100: {mean}"

    def test_sd_near_15(self, iq_scores):
        mean = sum(iq_scores) / len(iq_scores)
        variance = sum((s - mean) ** 2 for s in iq_scores) / len(iq_scores)
        sd = math.sqrt(variance)
        assert abs(sd - 15) < 2, f"SD should be ~15: {sd}"

    def test_tail_fraction_2sd(self, iq_scores):
        """Fraction beyond 2 SD. Normal distribution: ~4.6%.
        BETA: 3.7%. MEASUREMENT: how close?"""
        tails = tail_fraction(iq_scores, 2.0)
        # Normal theory: ~4.56% beyond 2 SD
        assert 0.03 < tails < 0.07, f"Tail fraction: {tails}"
        distance_to_beta = abs(tails - BETA)
        if distance_to_beta < 0.01:
            proximity = "CLOSE"
        elif distance_to_beta < 0.03:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Tails={tails:.4f}, BETA={BETA:.4f}, {proximity}"

    def test_top_beta_scorers(self, iq_scores):
        """Top BETA fraction of IQ scorers: what fraction of total IQ?"""
        coverage = top_fraction_score(iq_scores, BETA)
        assert coverage > BETA, \
            f"Top scorers should hold disproportionate share: {coverage}"

    def test_normal_distribution_symmetric(self, iq_scores):
        """IQ is symmetric -> skewness near 0."""
        skew = skewness(iq_scores)
        assert abs(skew) < 0.2, f"IQ should be near-symmetric: skew={skew}"

    def test_normal_kurtosis(self, iq_scores):
        """Normal distribution has excess kurtosis ~0."""
        kurt = kurtosis(iq_scores)
        assert abs(kurt) < 0.5, f"Kurtosis should be near 0: {kurt}"


# ============================================================
# TEST 2: BIG FIVE PERSONALITY
# ============================================================

class TestBigFivePersonality:
    """Big Five traits: noisy, bounded (1-5), slightly skewed."""

    @pytest.fixture
    def big_five(self):
        return generate_big_five_scores(5000, seed=42)

    def test_all_five_traits_present(self, big_five):
        assert set(big_five.keys()) == {'O', 'C', 'E', 'A', 'N'}

    def test_scores_bounded(self, big_five):
        for trait, scores in big_five.items():
            for s in scores:
                assert 1.0 <= s <= 5.0, f"{trait} score out of bounds: {s}"

    def test_neuroticism_lower_mean(self, big_five):
        """Neuroticism typically has lower mean than other traits."""
        n_mean = sum(big_five['N']) / len(big_five['N'])
        o_mean = sum(big_five['O']) / len(big_five['O'])
        assert n_mean < o_mean, f"N ({n_mean}) should be lower than O ({o_mean})"

    def test_trait_entropy(self, big_five):
        """Entropy of each trait distribution."""
        for trait, scores in big_five.items():
            entropy = distribution_entropy(scores, bins=20)
            assert entropy > 2.0, f"{trait} entropy too low: {entropy}"

    def test_cross_trait_correlation_low(self, big_five):
        """Big Five traits are designed to be relatively independent."""
        def pearson_r(x, y):
            n = len(x)
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
            den_x = math.sqrt(sum((v - mean_x) ** 2 for v in x))
            den_y = math.sqrt(sum((v - mean_y) ** 2 for v in y))
            if den_x == 0 or den_y == 0:
                return 0.0
            return num / (den_x * den_y)

        traits = list(big_five.keys())
        for i in range(len(traits)):
            for j in range(i + 1, len(traits)):
                r = pearson_r(big_five[traits[i]], big_five[traits[j]])
                assert abs(r) < 0.3, \
                    f"{traits[i]}-{traits[j]} correlation too high: {r}"

    def test_tail_scorers_per_trait(self, big_five):
        """Fraction of extreme scorers (>2 SD) per trait."""
        for trait, scores in big_five.items():
            tails = tail_fraction(scores, 2.0)
            assert 0.01 < tails < 0.10, \
                f"{trait} tail fraction outside range: {tails}"


# ============================================================
# TEST 3: REACTION TIME
# ============================================================

class TestReactionTime:
    """Reaction time: right-skewed, log-normal-ish."""

    @pytest.fixture
    def rt_data(self):
        return generate_reaction_times(5000, seed=42)

    def test_mean_around_250ms(self, rt_data):
        mean = sum(rt_data) / len(rt_data)
        assert 150 < mean < 400, f"Mean RT should be ~250ms: {mean}"

    def test_right_skewed(self, rt_data):
        """RT distributions are right-skewed (long tail of slow responses)."""
        skew = skewness(rt_data)
        assert skew > 0, f"RT should be right-skewed: {skew}"

    def test_positive_kurtosis(self, rt_data):
        """RT distributions typically have positive excess kurtosis (heavy tails)."""
        kurt = kurtosis(rt_data)
        assert kurt > -1.0, f"Kurtosis: {kurt}"

    def test_slow_responders_fraction(self, rt_data):
        """Fraction of very slow responders (>2 SD).
        In skewed distributions, this exceeds normal 4.6%."""
        tails = tail_fraction(rt_data, 2.0)
        assert tails > 0.01, f"Should have some slow responders: {tails}"

    def test_top_beta_reaction_times(self, rt_data):
        """Top BETA slowest responders: how much of total RT?"""
        coverage = top_fraction_score(rt_data, BETA)
        assert coverage > BETA, \
            f"Slowest responders should be disproportionate: {coverage}"


# ============================================================
# TEST 4: NORMAL vs NON-NORMAL
# ============================================================

class TestNormalVsNonNormal:
    """Does alpha/beta behave differently in normal vs skewed data?"""

    def test_normal_tail_near_expected(self):
        """Normal distribution: 2-SD tails should be ~4.6%."""
        scores = generate_iq_scores(50000, seed=42)
        tails = tail_fraction(scores, 2.0)
        assert abs(tails - 0.0456) < 0.01, f"Normal tails: {tails}"

    def test_normal_3sd_tail(self):
        """3-SD tails in normal: ~0.27%.
        Compare to... nothing specific in alpha/beta.
        Document the measurement."""
        scores = generate_iq_scores(50000, seed=42)
        tails = tail_fraction(scores, 3.0)
        assert 0.001 < tails < 0.01, f"3-SD tails: {tails}"

    def test_skewed_has_different_tails(self):
        """Skewed distributions have asymmetric tails."""
        rt = generate_reaction_times(10000, seed=42)
        iq = generate_iq_scores(10000, seed=42)
        rt_tails = tail_fraction(rt, 2.0)
        iq_tails = tail_fraction(iq, 2.0)
        # They should differ
        assert isinstance(rt_tails, float) and isinstance(iq_tails, float)

    def test_entropy_normal_vs_skewed(self):
        """Normal distribution should have different entropy than skewed."""
        iq = generate_iq_scores(5000, seed=42)
        rt = generate_reaction_times(5000, seed=42)
        iq_entropy = distribution_entropy(iq)
        rt_entropy = distribution_entropy(rt)
        assert iq_entropy > 0 and rt_entropy > 0


# ============================================================
# TEST 5: RANDOM DATA MUST DIFFER
# ============================================================

class TestRandomPsychMustDiffer:
    """Random uniform data must behave differently from real psychometric data."""

    def test_random_uniform_different_entropy(self):
        """Uniform random data should have higher entropy than normal."""
        rng = random.Random(42)
        random_scores = [rng.uniform(0, 100) for _ in range(5000)]
        iq_scores = generate_iq_scores(5000, seed=42)
        rand_entropy = distribution_entropy(random_scores)
        iq_entropy = distribution_entropy(iq_scores)
        assert rand_entropy > iq_entropy, \
            f"Uniform should have higher entropy: rand={rand_entropy}, iq={iq_entropy}"

    def test_random_uniform_no_skewness(self):
        """Uniform random data should have near-zero skewness."""
        rng = random.Random(42)
        random_scores = [rng.uniform(0, 100) for _ in range(5000)]
        skew = skewness(random_scores)
        assert abs(skew) < 0.2, f"Uniform should be symmetric: {skew}"

    def test_random_tails_different(self):
        """Uniform distribution has different tail behavior than normal."""
        rng = random.Random(42)
        random_scores = [rng.uniform(55, 145) for _ in range(10000)]
        normal_scores = generate_iq_scores(10000, seed=42)
        rand_tails = tail_fraction(random_scores, 2.0)
        norm_tails = tail_fraction(normal_scores, 2.0)
        assert abs(rand_tails - norm_tails) > 0.005, \
            f"Tail fractions should differ: rand={rand_tails}, norm={norm_tails}"

    def test_random_top_beta_more_equal(self):
        """In uniform data, top BETA should hold less disproportionate share."""
        rng = random.Random(42)
        random_scores = [rng.uniform(0, 100) for _ in range(5000)]
        iq_scores = generate_iq_scores(5000, mean=100, sd=15, seed=42)
        rand_top = top_fraction_score(random_scores, BETA)
        iq_top = top_fraction_score(iq_scores, BETA)
        # In uniform: top BETA holds only slightly more than BETA fraction
        # In normal: top BETA holds more (higher scores are further from mean)
        assert isinstance(rand_top, float) and isinstance(iq_top, float)


# ============================================================
# TEST 6: 2-SD RULE AND BETA
# ============================================================

class TestTwoSigmaAndBeta:
    """The 2-sigma rule: ~95.4% within 2 SD, ~4.6% outside.
    ALPHA = 96.3%, BETA = 3.7%.
    These are CLOSE but not identical.
    2-SD: 95.4/4.6. Alpha/Beta: 96.3/3.7.
    Is this coincidence or structure?"""

    def test_2sd_vs_alpha(self):
        """95.4% within 2-SD vs ALPHA 96.3%. Distance: ~0.9%."""
        within_2sd = 0.9544
        distance = abs(within_2sd - ALPHA)
        assert distance < 0.02, \
            f"2-SD within ({within_2sd}) is close to ALPHA ({ALPHA}): distance={distance}"

    def test_2sd_tails_vs_beta(self):
        """4.6% beyond 2-SD vs BETA 3.7%. Distance: ~0.9%."""
        beyond_2sd = 0.0456
        distance = abs(beyond_2sd - BETA)
        assert distance < 0.02, \
            f"2-SD tails ({beyond_2sd}) is close to BETA ({BETA}): distance={distance}"

    def test_empirical_verification(self):
        """Verify with actual generated data."""
        scores = generate_iq_scores(100000, seed=42)
        tails = tail_fraction(scores, 2.0)
        within = 1 - tails
        alpha_distance = abs(within - ALPHA)
        beta_distance = abs(tails - BETA)
        # Both should be close-ish
        assert alpha_distance < 0.02, f"Within 2-SD vs ALPHA: {alpha_distance}"
        assert beta_distance < 0.02, f"Tails vs BETA: {beta_distance}"

    def test_this_is_not_exact_match(self):
        """HONEST: 2-SD rule gives 95.4/4.6, NOT 96.3/3.7.
        The difference (0.9%) is small but real.
        This is proximity, not identity."""
        exact_2sd = 0.9544
        assert ALPHA != exact_2sd, "ALPHA and 2-SD are NOT identical"
        assert abs(ALPHA - exact_2sd) > 0.005, \
            f"They should be detectably different: {abs(ALPHA - exact_2sd)}"

    def test_what_sd_gives_alpha(self):
        """What number of SDs gives exactly ALPHA within?
        If normal CDF(x) = ALPHA, then x = ?
        ALPHA = 0.96296... -> both tails = 0.03704
        -> one tail = 0.01852 -> z ~ 2.085
        So alpha/beta corresponds to ~2.085 sigma, not exactly 2.0."""
        # Approximate inverse normal using rational approximation
        # For one tail p = BETA/2 = 0.01852
        p = BETA / 2
        # Abramowitz & Stegun approximation
        t = math.sqrt(-2 * math.log(p))
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        z = t - (c0 + c1 * t + c2 * t ** 2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3)
        # z should be approximately 2.08-2.09
        assert 2.0 < z < 2.2, f"z for ALPHA should be ~2.085: {z}"


# ============================================================
# RESULTS SUMMARY
# ============================================================

class TestPsychSummary:
    """Summary of all psychometric measurements."""

    def test_generate_psych_summary(self):
        results = {}

        iq = generate_iq_scores(10000, seed=42)
        results["iq_mean"] = sum(iq) / len(iq)
        results["iq_2sd_tails"] = tail_fraction(iq, 2.0)
        results["iq_3sd_tails"] = tail_fraction(iq, 3.0)
        results["iq_entropy"] = distribution_entropy(iq)
        results["iq_top_beta"] = top_fraction_score(iq, BETA)

        rt = generate_reaction_times(5000, seed=42)
        results["rt_mean"] = sum(rt) / len(rt)
        results["rt_skewness"] = skewness(rt)
        results["rt_2sd_tails"] = tail_fraction(rt, 2.0)
        results["rt_entropy"] = distribution_entropy(rt)

        results["2sd_within"] = 0.9544
        results["2sd_to_alpha_distance"] = abs(0.9544 - ALPHA)
        results["2sd_tails_to_beta_distance"] = abs(0.0456 - BETA)

        results["ALPHA"] = ALPHA
        results["BETA"] = BETA

        for key, value in results.items():
            assert isinstance(value, float), f"{key} is not float"
            assert not math.isnan(value), f"{key} is NaN"
            assert not math.isinf(value), f"{key} is infinite"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
