# Additional document candidates

Status: all choices below are proposed. No PDF has been downloaded or ingested, and no capture or model run has started. Word counts and token counts are unknown. In particular, page counts do not establish a greater-than-one-million-token context.

## Recommended single-document probe: Cerebras CS-1 research paper

**Fast Stencil-Code Computation on a Wafer-Scale Processor**, Kamil Rocki, Dirk Van Essendelft, Ilya Sharapov, Robert Schreiber, Michael Morrison, Vladimir Kibardin, Andrey Portnoy, Jean Francois Dietiker, Madhava Syamlal, and Michael James. arXiv v1, 7 October 2020; identified by the authors as an SC20 paper. [Primary landing page](https://arxiv.org/abs/2010.03660), [public PDF](https://arxiv.org/pdf/2010.03660). Verified length: 12 pages.

This is a compact architecture and systems probe rather than another broad evaluation. It covers the Cerebras CS-1 architecture and programming model, algorithm mapping, equations and pseudocode, measured results, a performance model, numerical precision, projections, comparisons, and stated limitations. It can expose failures in hardware hierarchy, spatial and algorithmic relationships, the distinction between measured and projected claims, and the attachment of caveats to comparisons.

The PDF has a readable text layer. Figures and tables are material, including architecture diagrams, mappings, scaling plots, and measured-result tables, so text-only capture would be an incomplete test. The arXiv record uses the [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/), which grants arXiv distribution rights but does not establish a general reuse or republication license. Treat redistribution rights as unknown beyond linking to the public source.

## Proposed fallback: Cerebras vendor architecture white paper

**Cerebras Systems: Achieving Industry Best AI Performance Through A Systems Approach**, White Paper 03. [Public PDF](https://cerebras.net/wp-content/uploads/2021/04/Cerebras-CS-2-Whitepaper.pdf). Verified length: 12 pages.

The paper covers the WSE-2, CS-2 power, cooling and I/O, the graph compiler, kernel placement, software tooling, and clustering. It is useful if a vendor-authored architecture document is preferred, but publisher claims and marketing language make the research paper above the stronger primary choice. Diagrams and product illustrations are important to the system description. No named individual author, explicit publication date, or general redistribution license was verified in the PDF. The `2021/04` URL path is not sufficient evidence of a publication date, so date and reuse rights remain unknown.

## Recommended small corpus: NIST post-quantum cryptography standards

Three final standards, all authored by the National Institute of Standards and Technology and dated 13 August 2024:

- **FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard**: [primary landing page](https://csrc.nist.gov/pubs/fips/203/final), [PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), 56 pages.
- **FIPS 204, Module-Lattice-Based Digital Signature Standard**: [primary landing page](https://csrc.nist.gov/pubs/fips/204/final), [PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), 65 pages.
- **FIPS 205, Stateless Hash-Based Digital Signature Standard**: [primary landing page](https://csrc.nist.gov/pubs/fips/205/final), [PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf), 61 pages.

Verified aggregate length: 182 pages. The corpus is coherent but contains distinct scopes: one key-encapsulation standard and two complementary signature standards. It stresses cross-document entity identity, shared notation and conventions, similar but distinct algorithms, parameter sets, normative requirements versus explanatory notes, qualified security claims, pseudocode, references, and version or errata drift. The FIPS 203 landing page records a 17 November 2025 planning note for a future correction. The FIPS 204 landing page records a 31 July 2026 errata note.

All three PDFs have readable text layers. Mathematical notation, algorithms, and tables are central; figures are less central than in the Cerebras probe but should remain available. NIST states that unmarked information on its sites is public information that may be copied or distributed, with appropriate credits requested, while warning that particular products can have their own terms. See [NIST Copyrights & Disclaimers](https://www.nist.gov/copyrights-disclaimers). Check each PDF for third-party material before redistributing extracted figures or substantial content.

## Interpretation limit

These are two convenient, deliberately different probes: one compact hardware and HPC paper, and one tightly scoped standards corpus. They can reveal capture failures outside marine geoscience, but they are not broad validation and should not be presented as such.
