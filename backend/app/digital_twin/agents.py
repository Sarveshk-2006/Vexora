import uuid
from typing import List

from app.core.enums import AgentStatus, AgentType
from app.digital_twin.seed import SeedManager
from app.models import PaymentAgent, User


class AgentGenerator:
    """Deterministic PaymentAgent synthetic population generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr

    def generate_agents(self, users: List[User], count: int) -> List[PaymentAgent]:
        """Generate N synthetic autonomous PaymentAgent actors."""
        agents: List[PaymentAgent] = []
        agent_types = list(AgentType)

        for i in range(1, count + 1):
            owner = self.seed_mgr.choice(users)
            agent_ref = f"SYN_AGENT_{i:06d}"

            agent = PaymentAgent(
                id=uuid.uuid4(),
                agent_reference=agent_ref,
                agent_type=self.seed_mgr.choice(agent_types),
                owner_user_id=owner.id,
                status=AgentStatus.ACTIVE,
            )
            agents.append(agent)

        return agents
