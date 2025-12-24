
import os
import logging
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from app.config.config import Config
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

class HypergraphService:
    def __init__(self, url: Optional[str] = None):
        self.url = url or Config.HYPERGRAPH_URL
        self.transport = AIOHTTPTransport(url=self.url)
        # Client will be initialized on first use to allow async context
        self.client = None

    async def _get_client(self):
        if not self.client:
             self.client = Client(transport=self.transport, fetch_schema_from_transport=False)
        return self.client

    async def create_strain_node(self, name: str, breeder_name: str, genetics_id: int) -> Optional[str]:
        """
        Creates a Strain node in the hypergraph and returns its UUID.
        """
        mutation = gql("""
            mutation CreateStrain($name: String!, $breederName: String!, $externalId: String!) {
                createStrain(input: {
                    name: $name, 
                    breederName: $breederName,
                    externalId: $externalId
                }) {
                    strain {
                        id
                    }
                }
            }
        """)
        
        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(mutation, variable_values={
                    "name": name,
                    "breederName": breeder_name,
                    "externalId": str(genetics_id)
                })
                return result["createStrain"]["strain"]["id"]
        except Exception as e:
            logger.error(f"Failed to create hypergraph strain node: {e}")
            return None

    async def create_breeder_node(self, name: str, website: Optional[str] = None, country: Optional[str] = None) -> Optional[str]:
        """
        Creates a Breeder node in the hypergraph and returns its UUID.
        """
        mutation = gql("""
            mutation CreateBreeder($name: String!, $website: String, $country: String) {
                createBreeder(input: {
                    name: $name,
                    website: $website,
                    country: $country
                }) {
                    breeder {
                        id
                    }
                }
            }
        """)
        
        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(mutation, variable_values={
                    "name": name,
                    "website": website,
                    "country": country
                })
                return result["createBreeder"]["breeder"]["id"]
        except Exception as e:
            logger.error(f"Failed to create hypergraph breeder node: {e}")
            return None

    async def get_ancestry_tree(self, node_id: str, depth: int = 5) -> Dict[str, Any]:
        """
        Retrieves the ancestry tree for a given strain node.
        """
        query = gql("""
            query GetAncestry($id: ID!, $depth: Int!) {
                strain(id: $id) {
                    name
                    ancestors(depth: $depth) {
                        name
                        generation
                        relationship
                    }
                }
            }
        """)
        
        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(query, variable_values={
                    "id": node_id,
                    "depth": depth
                })
                return result.get("strain", {})
        except Exception as e:
            logger.error(f"Failed to fetch ancestry tree: {e}")
            return {}

    async def get_legal_states(self, breeder_node_id: str) -> List[str]:
        """
        Returns a list of state codes where this breeder can ship.
        """
        query = gql("""
            query GetBreederCompliance($id: ID!) {
                breeder(id: $id) {
                    shippingRestrictions {
                        stateCode
                        allowed
                    }
                }
            }
        """)
        
        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(query, variable_values={"id": breeder_node_id})
                restrictions = result.get("breeder", {}).get("shippingRestrictions", [])
                # Return only allowed states
                return [r["stateCode"] for r in restrictions if r["allowed"]]
        except Exception as e:
            logger.error(f"Failed to fetch compliance data: {e}")
            return []

    async def add_parent_edge(self, child_node_id: str, parent_node_id: str, relationship_type: str = "parent") -> bool:
        """
        Creates a parent-child relationship between two strain nodes.
        """
        mutation = gql("""
            mutation AddParent($childId: ID!, $parentId: ID!, $type: String!) {
                addParent(input: {
                    childId: $childId,
                    parentId: $parentId,
                    type: $type
                }) {
                    success
                }
            }
        """)

        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(mutation, variable_values={
                    "childId": child_node_id,
                    "parentId": parent_node_id,
                    "type": relationship_type
                })
                return result.get("addParent", {}).get("success", False)
        except Exception as e:
            logger.error(f"Failed to add parent edge: {e}")
            return False

    async def add_terpene_edge(self, strain_node_id: str, terpene_name: str, percentage: float) -> bool:
        """
        Links a strain to a terpene node with a percentage weight.
        """
        mutation = gql("""
            mutation AddTerpene($strainId: ID!, $terpeneName: String!, $percentage: Float!) {
                addTerpene(input: {
                    strainId: $strainId,
                    terpeneName: $terpeneName,
                    percentage: $percentage
                }) {
                    success
                }
            }
        """)

        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(mutation, variable_values={
                    "strainId": strain_node_id,
                    "terpeneName": terpene_name,
                    "percentage": percentage
                })
                return result.get("addTerpene", {}).get("success", False)
        except Exception as e:
            logger.error(f"Failed to add terpene edge: {e}")
            return False

    async def get_descendants(self, node_id: str, depth: int = 3) -> Dict[str, Any]:
        """
        Retrieves descendants for a given strain node.
        """
        query = gql("""
            query GetDescendants($id: ID!, $depth: Int!) {
                strain(id: $id) {
                    name
                    descendants(depth: $depth) {
                        name
                        generation
                    }
                }
            }
        """)

        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(query, variable_values={
                    "id": node_id,
                    "depth": depth
                })
                return result.get("strain", {})
        except Exception as e:
            logger.error(f"Failed to fetch descendants: {e}")
            return {}

    async def get_common_ancestor(self, strain_id_1: str, strain_id_2: str) -> Optional[Dict[str, Any]]:
        """
        Finds the nearest common ancestor between two strains.
        """
        query = gql("""
            query CommonAncestor($id1: ID!, $id2: ID!) {
                commonAncestor(strainId1: $id1, strainId2: $id2) {
                    name
                    distance
                    id
                }
            }
        """)

        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(query, variable_values={
                    "id1": strain_id_1,
                    "id2": strain_id_2
                })
                return result.get("commonAncestor")
        except Exception as e:
            logger.error(f"Failed to find common ancestor: {e}")
            return None


    async def get_strain_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a strain node by its exact name.
        """
        query = gql("""
            query GetStrainByName($name: String!) {
                strains(where: { name: $name }, limit: 1) {
                    id
                    name
                    breederName
                    externalId
                }
            }
        """)
        
        try:
            client = await self._get_client()
            async with client as session:
                result = await session.execute(query, variable_values={"name": name})
                strains = result.get("strains", [])
                return strains[0] if strains else None
        except Exception as e:
            logger.error(f"Failed to find strain by name: {e}")
            return None
