from typing import Any, Dict, List, Optional

import networkx as nx

from app.blue_team.evidence import DetectorEvidence


class GraphIntelligenceDetector:
    """Graph Intelligence Detector using NetworkX graph topology analysis."""

    def __init__(self):
        self.graph = nx.Graph()
        self.device_user_counts: Dict[str, int] = {}
        self.merchant_user_counts: Dict[str, int] = {}

    def build_graph(self, digital_twin_result: Any) -> "GraphIntelligenceDetector":
        """Build synthetic graph from Digital Twin entities and relationships."""
        self.graph.clear()
        self.device_user_counts.clear()
        self.merchant_user_counts.clear()

        # Add Nodes & Edges
        users = getattr(digital_twin_result, "users", [])
        accounts = getattr(digital_twin_result, "accounts", [])
        devices = getattr(digital_twin_result, "devices", [])
        merchants = getattr(digital_twin_result, "merchants", [])
        transactions = getattr(digital_twin_result, "transactions", [])

        for u in users:
            self.graph.add_node(str(u.id), type="USER")

        for a in accounts:
            self.graph.add_node(str(a.id), type="ACCOUNT")
            self.graph.add_edge(str(a.user_id), str(a.id), rel="OWNABILITY")

        for d in devices:
            self.graph.add_node(str(d.id), type="DEVICE")

        for m in merchants:
            self.graph.add_node(str(m.id), type="MERCHANT")

        # Process transactions to construct interaction edges
        for tx in transactions:
            u_id = str(tx.user_id)
            d_id = str(tx.device_id)
            m_id = str(tx.merchant_id)

            if not self.graph.has_edge(u_id, d_id):
                self.graph.add_edge(u_id, d_id, rel="USAGE")

            if not self.graph.has_edge(u_id, m_id):
                self.graph.add_edge(u_id, m_id, rel="PAYMENT")

        # Calculate device and merchant concentration counts
        for d in devices:
            d_node = str(d.id)
            if self.graph.has_node(d_node):
                neighbors = list(self.graph.neighbors(d_node))
                user_neighbors = [
                    n for n in neighbors if self.graph.nodes[n].get("type") == "USER"
                ]
                self.device_user_counts[d_node] = len(user_neighbors)

        for m in merchants:
            m_node = str(m.id)
            if self.graph.has_node(m_node):
                neighbors = list(self.graph.neighbors(m_node))
                user_neighbors = [
                    n for n in neighbors if self.graph.nodes[n].get("type") == "USER"
                ]
                self.merchant_user_counts[m_node] = len(user_neighbors)

        return self

    def evaluate(
        self, tx: Any, feature_dict: Optional[Dict[str, Any]] = None
    ) -> DetectorEvidence:
        """Evaluate graph topology metrics for transaction."""
        if isinstance(tx, dict) and feature_dict is None:
            feature_dict = tx
            tx = None

        u_id = (
            str(tx.user_id)
            if (tx and hasattr(tx, "user_id"))
            else (str(feature_dict.get("user_id", "")) if feature_dict else "")
        )
        d_id = (
            str(tx.device_id)
            if (tx and hasattr(tx, "device_id"))
            else (str(feature_dict.get("device_id", "")) if feature_dict else "")
        )
        m_id = (
            str(tx.merchant_id)
            if (tx and hasattr(tx, "merchant_id"))
            else (str(feature_dict.get("merchant_id", "")) if feature_dict else "")
        )

        connected_entity_count = 1
        shared_device_count = 1
        merchant_concentration = 1
        community_size = 1
        reason_codes: List[str] = []
        graph_scores: List[float] = []

        if self.graph.has_node(u_id):
            connected_entity_count = len(list(self.graph.neighbors(u_id)))

        if d_id in self.device_user_counts:
            shared_device_count = self.device_user_counts[d_id]
            if shared_device_count >= 3:
                graph_scores.append(0.85)
                reason_codes.append("GRAPH_SHARED_DEVICE_HIGH_CONCENTRATION")
            elif shared_device_count == 2:
                graph_scores.append(0.50)
                reason_codes.append("GRAPH_SHARED_DEVICE_MODERATE")

        if m_id in self.merchant_user_counts:
            merchant_concentration = self.merchant_user_counts[m_id]

        if self.graph.has_node(u_id):
            # Compute local ego-subgraph component size
            comp = (
                list(nx.node_connected_component(self.graph, u_id))
                if self.graph.number_of_nodes() > 0
                else []
            )
            community_size = len(comp)

        raw_score = max(graph_scores) if graph_scores else 0.05
        risk_score = round(raw_score, 4)
        triggered = risk_score >= 0.50

        return DetectorEvidence(
            detector_name="GraphIntelligenceDetector",
            detector_version="1.0.0",
            risk_score=risk_score,
            confidence=0.85,
            triggered=triggered,
            reason_codes=reason_codes,
            feature_evidence={
                "connected_entity_count": connected_entity_count,
                "shared_device_count": shared_device_count,
                "merchant_concentration": merchant_concentration,
                "community_size": community_size,
            },
            metadata={
                "graph_nodes": self.graph.number_of_nodes(),
                "graph_edges": self.graph.number_of_edges(),
            },
        )
