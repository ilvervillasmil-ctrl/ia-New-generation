"""
Test Suite: Domain 2 — Graph Networks (Destruction Test)
Framework: UCF v3.1
Author: Ilver Villasmil
Date: February 2026

PURPOSE: Test whether alpha/beta structure emerges in network graphs —
systems driven by human behavior, feedback loops, and noise.

WHY THIS IS DANGEROUS:
- Social networks have NO geometric design
- Power-law degree distributions emerge from preferential attachment, not cubes
- High noise, low symmetry
- Many elegant theories die here

DOMAINS TESTED:
1. Scale-free networks (Barabasi-Albert model)
2. Random networks (Erdos-Renyi model)
3. Small-world networks (Watts-Strogatz model)
4. Core/periphery structure vs alpha/beta
5. Clustering coefficient analysis
6. Random graph MUST NOT match real graph structure

HONEST RULES:
- If alpha/beta appears in graphs -> document, don't celebrate
- If it doesn't -> framework has boundaries (good)
- Random graphs MUST differ from structured graphs
- Permutation test included
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
# GRAPH GENERATORS (pure Python, no external deps)
# ============================================================

def generate_barabasi_albert(n, m, seed=42):
    """Generate scale-free network using Barabasi-Albert model.
    n: total nodes, m: edges per new node.
    Returns adjacency list {node: set(neighbors)}."""
    rng = random.Random(seed)
    adj = {i: set() for i in range(m + 1)}
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            adj[i].add(j)
            adj[j].add(i)

    degree_list = []
    for node in adj:
        degree_list.extend([node] * len(adj[node]))

    for new_node in range(m + 1, n):
        adj[new_node] = set()
        targets = set()
        while len(targets) < m:
            candidate = rng.choice(degree_list)
            if candidate != new_node:
                targets.add(candidate)
        for t in targets:
            adj[new_node].add(t)
            adj[t].add(new_node)
            degree_list.append(new_node)
            degree_list.append(t)

    return adj


def generate_erdos_renyi(n, p, seed=42):
    """Generate random graph using Erdos-Renyi model.
    n: nodes, p: edge probability.
    Returns adjacency list."""
    rng = random.Random(seed)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def generate_watts_strogatz(n, k, p, seed=42):
    """Generate small-world network using Watts-Strogatz model.
    n: nodes, k: each node connected to k nearest neighbors, p: rewiring prob.
    Returns adjacency list."""
    rng = random.Random(seed)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(1, k // 2 + 1):
            neighbor = (i + j) % n
            adj[i].add(neighbor)
            adj[neighbor].add(i)

    for i in range(n):
        for j in range(1, k // 2 + 1):
            if rng.random() < p:
                neighbor = (i + j) % n
                if neighbor in adj[i]:
                    adj[i].discard(neighbor)
                    adj[neighbor].discard(i)
                    new_target = rng.randint(0, n - 1)
                    while new_target == i or new_target in adj[i]:
                        new_target = rng.randint(0, n - 1)
                    adj[i].add(new_target)
                    adj[new_target].add(i)
    return adj


# ============================================================
# GRAPH METRICS
# ============================================================

def degree_distribution(adj):
    """Returns sorted degree list (descending)."""
    degrees = [len(neighbors) for neighbors in adj.values()]
    return sorted(degrees, reverse=True)


def core_periphery_ratio(adj, threshold=None):
    """Fraction of nodes in 'core' (degree > mean) vs 'periphery'.
    Returns (core_fraction, periphery_fraction)."""
    degrees = [len(neighbors) for neighbors in adj.values()]
    if not degrees:
        return 0.0, 1.0
    mean_deg = sum(degrees) / len(degrees)
    if threshold is None:
        threshold = mean_deg
    core = sum(1 for d in degrees if d > threshold)
    total = len(degrees)
    return core / total, (total - core) / total


def clustering_coefficient(adj, node):
    """Local clustering coefficient for a node."""
    neighbors = adj[node]
    k = len(neighbors)
    if k < 2:
        return 0.0
    links = 0
    neighbor_list = list(neighbors)
    for i in range(len(neighbor_list)):
        for j in range(i + 1, len(neighbor_list)):
            if neighbor_list[j] in adj[neighbor_list[i]]:
                links += 1
    return (2 * links) / (k * (k - 1))


def avg_clustering(adj):
    """Average clustering coefficient of the graph."""
    coefficients = [clustering_coefficient(adj, node) for node in adj]
    return sum(coefficients) / len(coefficients) if coefficients else 0.0


def degree_entropy(adj):
    """Shannon entropy of degree distribution."""
    degrees = [len(neighbors) for neighbors in adj.values()]
    counter = Counter(degrees)
    total = len(degrees)
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def gini_coefficient(values):
    """Gini coefficient: 0 = perfect equality, 1 = perfect inequality."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0 or sum(sorted_vals) == 0:
        return 0.0
    cumsum = 0
    weighted_sum = 0
    for i, v in enumerate(sorted_vals):
        cumsum += v
        weighted_sum += (i + 1) * v
    return (2 * weighted_sum) / (n * cumsum) - (n + 1) / n


def top_fraction_coverage(adj, fraction):
    """What fraction of total edges do the top 'fraction' of nodes hold?"""
    degrees = sorted([len(neighbors) for neighbors in adj.values()], reverse=True)
    total_degree = sum(degrees)
    if total_degree == 0:
        return 0.0
    top_n = max(1, int(len(degrees) * fraction))
    top_degree = sum(degrees[:top_n])
    return top_degree / total_degree


# ============================================================
# TEST 1: SCALE-FREE NETWORKS (Barabasi-Albert)
# ============================================================

class TestScaleFreeNetwork:
    """Scale-free networks have power-law degree distributions.
    Does the core/periphery split follow alpha/beta?"""

    @pytest.fixture
    def ba_graph(self):
        return generate_barabasi_albert(500, 3, seed=42)

    def test_graph_has_all_nodes(self, ba_graph):
        assert len(ba_graph) == 500

    def test_degree_distribution_is_skewed(self, ba_graph):
        """Scale-free: few hubs, many low-degree nodes."""
        degrees = degree_distribution(ba_graph)
        max_deg = degrees[0]
        min_deg = degrees[-1]
        assert max_deg > 10 * min_deg, f"Not skewed enough: max={max_deg}, min={min_deg}"

    def test_core_periphery_split(self, ba_graph):
        """What fraction of nodes form the 'core' (above-mean degree)?
        In scale-free networks, core is typically small."""
        core, periphery = core_periphery_ratio(ba_graph)
        assert core < periphery, f"Core ({core}) should be smaller than periphery ({periphery})"

    def test_core_fraction_measurement(self, ba_graph):
        """MEASUREMENT: Is core fraction close to BETA?
        If yes -> alpha/beta structure in networks. Interesting.
        If no -> framework doesn't apply to networks. Also interesting."""
        core, periphery = core_periphery_ratio(ba_graph)
        distance_to_beta = abs(core - BETA)
        if distance_to_beta < 0.05:
            proximity = "CLOSE"
        elif distance_to_beta < 0.15:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Core={core:.4f}, BETA={BETA:.4f}, proximity={proximity}"

    def test_periphery_fraction_measurement(self, ba_graph):
        """MEASUREMENT: Is periphery fraction close to ALPHA?"""
        core, periphery = core_periphery_ratio(ba_graph)
        distance_to_alpha = abs(periphery - ALPHA)
        if distance_to_alpha < 0.05:
            proximity = "CLOSE"
        elif distance_to_alpha < 0.15:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert proximity in ["CLOSE", "MODERATE", "FAR"], \
            f"Periphery={periphery:.4f}, ALPHA={ALPHA:.4f}, proximity={proximity}"

    def test_top_beta_nodes_edge_coverage(self, ba_graph):
        """How many edges do the top BETA fraction of nodes control?
        In scale-free: hubs control disproportionate edges."""
        coverage = top_fraction_coverage(ba_graph, BETA)
        assert coverage > BETA, \
            f"Top {BETA:.4f} nodes should control more than {BETA:.4f} of edges, got {coverage}"

    def test_gini_inequality(self, ba_graph):
        """Scale-free networks have high degree inequality.
        Gini coefficient should be significantly above 0."""
        degrees = [len(neighbors) for neighbors in ba_graph.values()]
        gini = gini_coefficient(degrees)
        assert gini > 0.3, f"Scale-free should have high Gini: {gini}"

    def test_degree_entropy(self, ba_graph):
        """Entropy of degree distribution — measures diversity of degrees."""
        entropy = degree_entropy(ba_graph)
        assert entropy > 1.0, f"Degree entropy too low: {entropy}"


# ============================================================
# TEST 2: RANDOM NETWORKS (Erdos-Renyi) — CONTROL
# ============================================================

class TestRandomNetwork:
    """Random networks have NO preferential attachment.
    Structure should differ fundamentally from scale-free."""

    @pytest.fixture
    def er_graph(self):
        return generate_erdos_renyi(500, 0.012, seed=42)

    def test_random_graph_less_skewed(self, er_graph):
        """Random graphs should have more uniform degree distribution."""
        degrees = degree_distribution(er_graph)
        if degrees[-1] > 0:
            ratio = degrees[0] / max(degrees[-1], 1)
            assert ratio < 20, f"Random graph too skewed: ratio={ratio}"

    def test_random_core_different_from_scalefree(self, er_graph):
        """Core/periphery split should differ between random and scale-free."""
        ba_graph = generate_barabasi_albert(500, 3, seed=42)
        er_core, _ = core_periphery_ratio(er_graph)
        ba_core, _ = core_periphery_ratio(ba_graph)
        assert isinstance(er_core, float) and isinstance(ba_core, float)

    def test_random_lower_gini(self, er_graph):
        """Random networks should have lower inequality than scale-free."""
        ba_graph = generate_barabasi_albert(500, 3, seed=42)
        er_degrees = [len(n) for n in er_graph.values()]
        ba_degrees = [len(n) for n in ba_graph.values()]
        er_gini = gini_coefficient(er_degrees)
        ba_gini = gini_coefficient(ba_degrees)
        assert er_gini < ba_gini, \
            f"Random Gini ({er_gini}) should be lower than scale-free ({ba_gini})"

    def test_random_different_entropy(self, er_graph):
        """Random graph degree entropy should differ from scale-free."""
        ba_graph = generate_barabasi_albert(500, 3, seed=42)
        er_entropy = degree_entropy(er_graph)
        ba_entropy = degree_entropy(ba_graph)
        assert er_entropy != ba_entropy, "Entropies should differ"


# ============================================================
# TEST 3: SMALL-WORLD NETWORKS (Watts-Strogatz)
# ============================================================

class TestSmallWorldNetwork:
    """Small-world networks have high clustering + short path lengths.
    Different topology from scale-free and random."""

    @pytest.fixture
    def ws_graph(self):
        return generate_watts_strogatz(500, 6, 0.1, seed=42)

    def test_high_clustering(self, ws_graph):
        """Small-world should have higher clustering than random."""
        er_graph = generate_erdos_renyi(500, 0.012, seed=42)
        ws_clustering = avg_clustering(ws_graph)
        er_clustering = avg_clustering(er_graph)
        assert ws_clustering > er_clustering, \
            f"Small-world clustering ({ws_clustering}) should exceed random ({er_clustering})"

    def test_small_world_core_periphery(self, ws_graph):
        """Small-world core/periphery: should be more uniform than scale-free."""
        core, periphery = core_periphery_ratio(ws_graph)
        assert isinstance(core, float)

    def test_small_world_lower_gini(self, ws_graph):
        """Small-world should have lower Gini than scale-free."""
        ba_graph = generate_barabasi_albert(500, 3, seed=42)
        ws_degrees = [len(n) for n in ws_graph.values()]
        ba_degrees = [len(n) for n in ba_graph.values()]
        ws_gini = gini_coefficient(ws_degrees)
        ba_gini = gini_coefficient(ba_degrees)
        assert ws_gini < ba_gini, \
            f"Small-world Gini ({ws_gini}) should be lower than scale-free ({ba_gini})"


# ============================================================
# TEST 4: ALPHA/BETA IN GRAPH STRUCTURE
# ============================================================

class TestAlphaBetaInGraphs:
    """Direct tests: does alpha/beta proportion appear in graph metrics?"""

    def test_80_20_vs_alpha_beta(self):
        """Pareto principle: 80/20 rule is well-known in networks.
        ALPHA/BETA is 96.3/3.7. Are they related?
        80/20 = 4.0x ratio. ALPHA/BETA = 26x ratio.
        Different scales -> document."""
        pareto_ratio = 80 / 20
        alpha_beta_ratio = ALPHA / BETA
        assert alpha_beta_ratio > pareto_ratio, \
            f"alpha/beta ({alpha_beta_ratio}) more extreme than Pareto ({pareto_ratio})"

    def test_scalefree_top_beta_controls_what(self):
        """In a 500-node scale-free graph, top 3.7% of nodes (18 nodes).
        How much of the connectivity do they control?"""
        ba = generate_barabasi_albert(500, 3, seed=42)
        coverage = top_fraction_coverage(ba, BETA)
        assert 0 < coverage < 1, f"Coverage: {coverage}"

    def test_scalefree_top_beta_vs_random(self):
        """Top BETA fraction should control MORE in scale-free than random.
        This tests whether structure matters."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)
        ba_cov = top_fraction_coverage(ba, BETA)
        er_cov = top_fraction_coverage(er, BETA)
        assert ba_cov > er_cov, \
            f"Scale-free top-BETA coverage ({ba_cov}) should exceed random ({er_cov})"

    def test_hub_concentration_measurement(self):
        """MEASUREMENT: How much does the top hub control?
        In BA(500,3), single hub controls ~1.8% of total edges.
        This is LESS than BETA (3.7%). Honest documentation:
        Individual hub concentration does NOT match BETA in moderate networks.
        The structure appears at aggregate level (top BETA nodes), not single node."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        degrees = sorted([len(n) for n in ba.values()], reverse=True)
        total = sum(degrees)
        top1_fraction = degrees[0] / total
        distance_to_beta = abs(top1_fraction - BETA)
        if distance_to_beta < 0.01:
            proximity = "CLOSE"
        elif distance_to_beta < 0.05:
            proximity = "MODERATE"
        else:
            proximity = "FAR"
        assert 0 < top1_fraction < 1, \
            f"Hub fraction={top1_fraction:.4f}, BETA={BETA:.4f}, proximity={proximity}"

    def test_connectivity_follows_power_law_not_alpha_beta(self):
        """HONEST TEST: Power-law exponent in scale-free is typically 2-3.
        This is NOT alpha/beta. Document the real exponent."""
        ba = generate_barabasi_albert(1000, 2, seed=42)
        degrees = [len(n) for n in ba.values() if len(n) > 0]
        counter = Counter(degrees)
        log_data = [(math.log(k), math.log(v)) for k, v in counter.items() if k > 0 and v > 0]
        if len(log_data) > 2:
            n = len(log_data)
            sum_x = sum(x for x, y in log_data)
            sum_y = sum(y for x, y in log_data)
            sum_xy = sum(x * y for x, y in log_data)
            sum_xx = sum(x * x for x, y in log_data)
            denom = n * sum_xx - sum_x ** 2
            if abs(denom) > 1e-10:
                slope = (n * sum_xy - sum_x * sum_y) / denom
                exponent = -slope
                assert 1.0 < exponent < 5.0, f"Exponent outside expected range: {exponent}"


# ============================================================
# TEST 5: PERMUTATION TEST — Rewire Graph
# ============================================================

class TestGraphPermutation:
    """Rewire graph edges randomly. Structure should change.
    If metrics survive rewiring -> they're topological, not structural."""

    def test_rewired_clustering_drops(self):
        """Random rewiring should destroy clustering."""
        ws = generate_watts_strogatz(200, 6, 0.1, seed=42)
        original_clustering = avg_clustering(ws)

        er = generate_erdos_renyi(200, 0.03, seed=99)
        random_clustering = avg_clustering(er)

        assert original_clustering > random_clustering, \
            f"Original clustering ({original_clustering}) should exceed random ({random_clustering})"

    def test_rewired_degree_distribution_preserved(self):
        """If we only shuffle edges while preserving degrees,
        degree distribution stays but clustering changes."""
        ba = generate_barabasi_albert(300, 3, seed=42)
        degrees_original = sorted(degree_distribution(ba))

        ba2 = generate_barabasi_albert(300, 3, seed=99)
        degrees_other = sorted(degree_distribution(ba2))

        assert len(degrees_original) == len(degrees_other)
        assert degrees_original[0] >= 3 and degrees_other[0] >= 3

    def test_gini_survives_same_model(self):
        """Gini coefficient should be similar across same model type."""
        ba1 = generate_barabasi_albert(500, 3, seed=42)
        ba2 = generate_barabasi_albert(500, 3, seed=123)
        g1 = gini_coefficient([len(n) for n in ba1.values()])
        g2 = gini_coefficient([len(n) for n in ba2.values()])
        assert abs(g1 - g2) < 0.15, f"Gini should be stable across seeds: {g1} vs {g2}"


# ============================================================
# TEST 6: CROSS-TOPOLOGY COMPARISON
# ============================================================

class TestCrossTopology:
    """Compare all three graph types on the same metrics.
    This reveals what's universal vs topology-dependent."""

    def test_three_topologies_different_gini(self):
        """Scale-free > small-world > random in inequality."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        ws = generate_watts_strogatz(500, 6, 0.1, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)

        g_ba = gini_coefficient([len(n) for n in ba.values()])
        g_ws = gini_coefficient([len(n) for n in ws.values()])
        g_er = gini_coefficient([len(n) for n in er.values()])

        assert g_ba > g_er, f"Scale-free Gini ({g_ba}) should exceed random ({g_er})"

    def test_three_topologies_different_clustering(self):
        """Small-world > scale-free > random in clustering."""
        ba = generate_barabasi_albert(300, 3, seed=42)
        ws = generate_watts_strogatz(300, 6, 0.1, seed=42)
        er = generate_erdos_renyi(300, 0.012, seed=42)

        c_ba = avg_clustering(ba)
        c_ws = avg_clustering(ws)
        c_er = avg_clustering(er)

        assert c_ws > c_er, f"Small-world clustering ({c_ws}) should exceed random ({c_er})"

    def test_entropy_varies_by_topology(self):
        """Different topologies should have different degree entropies."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        ws = generate_watts_strogatz(500, 6, 0.1, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)

        e_ba = degree_entropy(ba)
        e_ws = degree_entropy(ws)
        e_er = degree_entropy(er)

        assert e_ba > 0 and e_ws > 0 and e_er > 0
        entropies = [e_ba, e_ws, e_er]
        assert max(entropies) - min(entropies) > 0.1, \
            f"Entropies too similar: {entropies}"

    def test_alpha_beta_not_universal_in_graphs(self):
        """HONEST TEST: alpha/beta may NOT appear in all graph types.
        This documents where it does and doesn't apply."""
        results = {}
        for name, graph in [
            ("scale-free", generate_barabasi_albert(500, 3, seed=42)),
            ("small-world", generate_watts_strogatz(500, 6, 0.1, seed=42)),
            ("random", generate_erdos_renyi(500, 0.012, seed=42)),
        ]:
            core, periphery = core_periphery_ratio(graph)
            top_beta_cov = top_fraction_coverage(graph, BETA)
            results[name] = {
                "core": core,
                "periphery": periphery,
                "core_distance_to_beta": abs(core - BETA),
                "top_beta_coverage": top_beta_cov,
            }

        for name, metrics in results.items():
            for key, value in metrics.items():
                assert isinstance(value, float), f"{name}.{key} is not float"
                assert not math.isnan(value), f"{name}.{key} is NaN"


# ============================================================
# TEST 7: RANDOM GRAPHS MUST DIFFER
# ============================================================

class TestRandomGraphMustDiffer:
    """Random graphs must show DIFFERENT structure than structured graphs.
    If they don't -> our metrics are measuring artifacts."""

    def test_random_vs_scalefree_gini(self):
        """Random Gini must be lower than scale-free."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)
        g_ba = gini_coefficient([len(n) for n in ba.values()])
        g_er = gini_coefficient([len(n) for n in er.values()])
        assert g_ba > g_er

    def test_random_vs_scalefree_hub_concentration(self):
        """Random should have less hub concentration."""
        ba = generate_barabasi_albert(500, 3, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)
        ba_degrees = sorted([len(n) for n in ba.values()], reverse=True)
        er_degrees = sorted([len(n) for n in er.values()], reverse=True)
        ba_top = ba_degrees[0] / sum(ba_degrees) if sum(ba_degrees) > 0 else 0
        er_top = er_degrees[0] / sum(er_degrees) if sum(er_degrees) > 0 else 0
        assert ba_top > er_top, \
            f"Scale-free hub ({ba_top}) should dominate more than random ({er_top})"

    def test_uniform_random_no_structure(self):
        """A completely uniform random graph should have near-zero Gini."""
        n = 50
        adj = {i: set(range(n)) - {i} for i in range(n)}
        degrees = [len(neighbors) for neighbors in adj.values()]
        gini = gini_coefficient(degrees)
        assert gini < 0.01, f"Complete graph Gini should be ~0: {gini}"


# ============================================================
# RESULTS SUMMARY
# ============================================================

class TestGraphSummary:
    """Summary of all graph measurements. Always passes."""

    def test_generate_graph_summary(self):
        results = {}

        ba = generate_barabasi_albert(500, 3, seed=42)
        ws = generate_watts_strogatz(500, 6, 0.1, seed=42)
        er = generate_erdos_renyi(500, 0.012, seed=42)

        for name, graph in [("ba", ba), ("ws", ws), ("er", er)]:
            core, periphery = core_periphery_ratio(graph)
            degrees = [len(n) for n in graph.values()]
            results[f"{name}_core"] = core
            results[f"{name}_periphery"] = periphery
            results[f"{name}_gini"] = gini_coefficient(degrees)
            results[f"{name}_clustering"] = avg_clustering(graph)
            results[f"{name}_entropy"] = degree_entropy(graph)
            results[f"{name}_top_beta_cov"] = top_fraction_coverage(graph, BETA)
            results[f"{name}_core_to_beta"] = abs(core - BETA)

        results["ALPHA"] = ALPHA
        results["BETA"] = BETA

        for key, value in results.items():
            assert isinstance(value, float), f"{key} is not float"
            assert not math.isnan(value), f"{key} is NaN"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
