from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from bpx.types.blockchain_format.foliage import Foliage
from bpx.types.blockchain_format.reward_chain_block import RewardChainBlock
from bpx.types.blockchain_format.sized_bytes import bytes32
from bpx.types.blockchain_format.vdf import VDFProof
from bpx.types.end_of_slot_bundle import EndOfSubSlotBundle
from bpx.util.ints import uint32, uint128
from bpx.util.streamable import Streamable, streamable
from bpx.types.blockchain_format.execution_payload import ExecutionPayloadV2


@streamable
@dataclass(frozen=True)
class HeaderBlock(Streamable):
    finished_sub_slots: List[EndOfSubSlotBundle]  # If first sb
    reward_chain_block: RewardChainBlock  # Reward chain trunk data
    challenge_chain_sp_proof: Optional[VDFProof]  # If not first sp in sub-slot
    challenge_chain_ip_proof: VDFProof
    reward_chain_sp_proof: Optional[VDFProof]  # If not first sp in sub-slot
    reward_chain_ip_proof: VDFProof
    infused_challenge_chain_ip_proof: Optional[VDFProof]  # Iff deficit < 4
    foliage: Foliage  # Reward chain foliage data
    execution_payload: Optional[ExecutionPayloadV2]

    @property
    def prev_header_hash(self) -> bytes32:
        return self.foliage.prev_block_hash

    @property
    def prev_hash(self) -> bytes32:
        return self.foliage.prev_block_hash

    @property
    def height(self) -> uint32:
        return self.reward_chain_block.height

    @property
    def weight(self) -> uint128:
        return self.reward_chain_block.weight

    @property
    def header_hash(self) -> bytes32:
        return self.foliage.get_hash()

    @property
    def total_iters(self) -> uint128:
        return self.reward_chain_block.total_iters

    @property
    def log_string(self) -> str:
        return "block " + str(self.header_hash) + " sb_height " + str(self.height) + " "

    @property
    def first_in_sub_slot(self) -> bool:
        return self.finished_sub_slots is not None and len(self.finished_sub_slots) > 0
