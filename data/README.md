# Dataset setup

The experiments use the labeled **contact-high-school** hypergraph from the Cornell Higher-Order Network Data collection.

1. Open the [official dataset page](https://www.cs.cornell.edu/~arb/data/contact-high-school-labeled/).
2. Follow its download link.
3. Place the hyperedge file at:

   ```text
   data/contact-high-school/hyperedges-contact-high-school.txt
   ```

Each non-empty line is parsed as one comma-separated hyperedge. Node identifiers are kept as strings.

Raw data are intentionally excluded from this repository because the official page does not state a repository-compatible redistribution license.

## Dataset statistics

The official page reports 327 nodes, 7,818 hyperedges, mean/median hyperedge size 2.3/2, rank 5, and nine node classes. The data represent groups of people detected in proximity by wearable sensors at a high school.

## Citations requested by the dataset provider

```bibtex
@article{chodrow2021hypergraph,
  title   = {Hypergraph clustering: from blockmodels to modularity},
  author  = {Chodrow, Philip S. and Veldt, Nate and Benson, Austin R.},
  journal = {Science Advances},
  year    = {2021}
}

@article{mastrandrea2015contact,
  title   = {Contact Patterns in a High School: A Comparison between Data Collected Using Wearable Sensors, Contact Diaries and Friendship Surveys},
  author  = {Mastrandrea, Rossana and Fournet, Julie and Barrat, Alain},
  journal = {PLOS ONE},
  year    = {2015},
  doi     = {10.1371/journal.pone.0136497}
}
```

