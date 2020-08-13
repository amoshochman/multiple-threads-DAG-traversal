# multiple-threads-DAG-traversal

## An implementation of a simple multiple-threads traversal of a Directed Acyclic Graph. 

<br/> File main.py: the implementation of the relevant class, Graph. (And the almost trivial one, Node).
<br/> File test.py: a basic demonstration.
<br/>
<br/>
Given a DAG G, G.traverse() will visit the nodes (that is, call the associated function with each node) in G in the following way:
starting from the root of the graph, will visit in parallel (that is, using multiple threads) every node N such that all the parents of N were visited.
