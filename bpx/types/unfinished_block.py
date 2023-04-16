from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from bpx.types.blockchain_format.foliage import Foliage
from bpx.types.blockchain_format.reward_chain_block import RewardChainBlockUnfinished
from bpx.types.blockchain_format.sized_bytes import bytes32
from bpx.types.blockchain_format.vdf import VDFProof
from bpx.types.end_of_slot_bundle import EndOfSubSlotBundle
from bpx.util.ints import uint32, uint128
from bpx.util.streamable import Streamable, streamable


@streamable
@dataclass(frozen=True)
class UnfinishedBlock(Streamable):
    # Full block, without the final VDFs
    finished_sub_slots: List[EndOfSubSlotBundle]  # If first sb
    reward_chain_block: RewardChainBlockUnfinished  # Reward chain trunk data
    challenge_chain_sp_proof: Optional[VDFProof]  # If not first sp in sub-slot
    reward_chain_sp_proof: Optional[VDFProof]  # If not first sp in sub-slot
    foliage: Foliage  # Reward chain foliage data
    payload: Optional[Dict[str, Any]]

    @property
    def prev_header_hash(self) -> bytes32:
        return self.foliage.prev_block_hash

    @property
    def partial_hash(self) -> bytes32:
        return self.reward_chain_block.get_hash()

    @property
    def total_iters(self) -> uint128:
        return self.reward_chain_block.total_iters
