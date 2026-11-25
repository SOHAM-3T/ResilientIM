# ResilientIM

**Resilient Influence Maximization** is a research implementation for studying influence maximization under community-level welfare constraints and uncertainty.

> **Development status:** Milestone 1 (project setup) is in progress. This repository currently provides project metadata and a reproducible synthetic graph generator. Diffusion, RR sampling, estimators, confidence procedures, R-FEAS, HFPO, baselines, and experiments are planned work and are not yet implemented. No experimental results or algorithmic guarantees are claimed by this scaffold.

## Research motivation

Influence maximization traditionally selects a limited number of seed nodes to maximize expected spread. In community-aware settings, high total spread can coexist with poor outcomes for smaller or less connected groups. ResilientIM is intended to study the trade-off between total influence and a minimum level of community welfare, while accounting for uncertainty in estimates.

## Problem formulation

Let a directed graph be (G=(V,E)), partitioned into disjoint communities (C_1,\ldots,C_m). Under Independent Cascade (IC), each edge ((u,v)) has an activation probability (p_{uv}). For seed set (S), let (A_\infty(S,\omega)) be the final active set in random realization \(\omega\). The intended objective is

\[
f(S)=\mathbb E[|A_\infty(S,\omega)|],\qquad |S|\le K,
\]

subject to community welfare

\[
r_c(S)=\frac{\mathbb E[|A_\infty(S,\omega)\cap C_c|]}{|C_c|},\qquad
g(S)=\sum_{c=1}^{m}w_c\log\left(1+\frac{r_c(S)}{\eta}\right)\ge\tau,
\]

where (w_c\ge0), \(\eta>0\), and the weights remain fixed within an experiment. Under IC, expected influence and expected community coverage are monotone submodular. The stated nonnegative weighted sum of nondecreasing concave transforms of coverage is also monotone submodular. This does **not** imply that the complete welfare-constrained problem, or HFPO, inherits the standard cardinality-constrained greedy (1-1/e) guarantee.

## Planned algorithm architecture

The intended implementation will combine:

- **IC diffusion** for forward simulation and independent validation.
- **Community-rooted reverse-reachable (RR) sampling** for scalable coverage and influence estimation. Community-rooted targets sampled uniformly make the community coverage estimator unbiased. Applying the logarithm to estimated coverage yields a plug-in welfare estimator that is generally downward-biased; it will not be described as unbiased.
- **R-FEAS** (Resilient Feasibility Evaluation) to classify candidates as certified feasible, certified infeasible, or unresolved using confidence bounds and additional samples.
- **HFPO** (Hybrid Feasibility–Pareto Optimization) to generate welfare-oriented candidates, refine feasibility, complete candidates for influence, and retain non-dominated influence–welfare outcomes. These search choices are heuristics unless a separate proof is established.
- **Independent validation** using fresh samples not used to generate the candidate pool.

### R-FEAS decision rule (planned)

```text
for each sampling stage t:
    estimate community coverage and simultaneous welfare bounds [g_L, g_U]
    if g_L >= tau: return CERTIFIED_FEASIBLE
    if g_U < tau:  return CERTIFIED_INFEASIBLE
    if sample/stage budget is exhausted: return UNCERTAIN
    extend the existing sample streams and refine
```

An unresolved candidate is never labeled infeasible. Repeated stages require sequential error allocation; the planned schedule is \(\delta_t=6\delta/(\pi^2t^2)\), which sums to \(\delta\). A union bound over all seed sets of size at most (K) can be conservative. A smaller candidate-pool bound is valid only when that pool is chosen independently of validation samples. Fixed-candidate confidence intervals do not automatically cover adaptively selected candidates.

For fixed candidates, Hoeffding gives \(\epsilon_c=\sqrt{\log(2/\delta_c)/(2\theta_c)}\) for \(\theta_c\) community samples. Clipping \(\hat r_c\pm\epsilon_c\) to \([0,1]\) and applying the increasing welfare transform gives welfare bounds under simultaneous coverage. The plug-in welfare estimate is distinct from those bounds. The planned sufficient allocation scalings, \(\theta_c\propto w_c^{2/3}\) for the stated welfare bound and \(\theta_c\propto |C_c|\) for influence, depend on their continuous relaxation and bound assumptions; integer caps and minimum counts need explicit handling.

## Repository layout

```text
configs/                 YAML experiment defaults
data/{raw,processed,synthetic}/  dataset locations (data files are not committed)
src/resilientim/         installable Python package
tests/                   mathematical and behavioral tests
notebooks/               exploratory analysis
results/{tables,figures,logs}/   generated outputs (not committed)
```

As the project advances, the package will be organized into graph, diffusion, RR sampling, estimators, algorithms, validation, and experiments modules. Those modules are intentionally absent until their milestones.

## Installation

Python 3.10 or newer is required.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Quick start: synthetic graph

```python
from resilientim.graph.synthetic import make_synthetic_graph

graph = make_synthetic_graph(
    num_communities=3,
    nodes_per_community=20,
    within_community_probability=0.12,
    cross_community_probability=0.02,
    seed=7,
)
print(graph.number_of_nodes(), graph.number_of_edges())
```

The generator creates a directed stochastic block graph, includes isolated nodes, stores each node's integer community ID in the `community` attribute, and uses a local seeded random generator. It describes graph topology only; it does not simulate diffusion or assign IC probabilities to edges.

## Data and experiments

Synthetic defaults are in `configs/synthetic.yaml`. Real datasets (planned examples: NetHEPT, Epinions, and Wiki-Vote) must be obtained from their authoritative sources and placed in `data/raw/`; this repository does not bundle them or assert dataset statistics. Dataset loaders and preprocessing conventions will be documented when implemented. Experiment commands and CSV/JSON result outputs are planned for a later milestone.

Every future experiment should record dataset and graph dimensions, community sizes, probability configuration, (K), \(\tau\), \(\eta\), welfare weights, sampling parameters, random seed, and algorithm version. Results should be independently validated and not inferred from a single run.

## Tests

```bash
pytest -q
```

Milestone 1 tests cover synthetic graph parameter validation, community partitioning, and reproducibility. Statistical and algorithmic tests will be added with their corresponding implementations.

## Limitations and research integrity

This setup milestone is not an experimentally validated framework. No baseline performance, runtime improvement, dataset statistic, or HFPO approximation guarantee is asserted. Candidate generation and Pareto search are intended as heuristics. A greedy cover exceeding (K) cannot establish infeasibility; a candidate exactly at the threshold may remain unresolved; and confidence procedures must account for adaptivity and repeated looks.

## Planned next steps

1. Implement and verify IC simulation and live-edge/RR sampling on hand-checkable graphs.
2. Add estimators, sample allocation, and confidence bounds with statistical validation.
3. Implement sequential R-FEAS and unresolved-candidate handling.
4. Implement HFPO candidate generation, influence completion, and Pareto filtering.
5. Add baselines, independent experiments, ablations, and research visualizations.

## Citation

Citation placeholder — replace with the final paper citation when available.
