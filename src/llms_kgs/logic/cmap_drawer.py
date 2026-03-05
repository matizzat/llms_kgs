from pyvis.network import Network
from pyvis import network as net
from llms_kgs.domain import CMap, Triple

import networkx as nx
from typing import List

class CMapDrawer:
    """
    Responsible of transforming CMap objets into
    Pyvis networks for concept map visualization. 
    """

    @staticmethod
    def _add_to_graph(cmap: CMap, G: nx.MultiDiGraph, highlights: List[Triple]):

        """ 
        Adds a cmap into a networkx graph.
        """
        for triple in cmap.triples:
                
            s = triple.source.label 
            r = triple.relation.label 
            t = triple.target.label

            if(s not in G):
                G.add_node(s, label=s, color = 'black')

            if(t not in G):
                G.add_node(t, label=t, color = 'black')

            color = 'blue'
            width = 1

            for target in highlights:
            
                if triple.equal_to(target):

                    color = 'red'
                    width = 3
                    break

            G.add_edge(
                s,
                t, 
                label=r,
                title = cmap.focus_question,
                color = color,
                width = width 
            )

    @staticmethod
    def draw(cmaps: List[CMap], highlights: List[Triple] = []) -> Network:
        """ 
        Creates a Pyvis network from cmap. 
        """

        G = nx.MultiDiGraph()

        for cmap in cmaps:
            CMapDrawer._add_to_graph(cmap, G, highlights)

        vis = net.Network(directed=True)
        vis.from_nx(G)
        
        return vis

