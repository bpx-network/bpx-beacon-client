from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from typing_extensions import Protocol

from bpx.consensus.constants import ConsensusConstants
from bpx.consensus.pot_iterations import calculate_ip_iters, calculate_sp_iters
from bpx.types.blockchain_format.classgroup import ClassgroupElement
from bpx.types.blockchain_format.sized_bytes import bytes32
from bpx.types.blockchain_format.sub_epoch_summary import SubEpochSummary
from bpx.util.ints import uint8, uint32, uint64, uint128
from bpx.util.streamable import Streamable, streamable


class BlockRecordProtocol(Protocol):
    @property
    def header_hash(self) -> bytes32:
        ...

    @property
    def height(self) -> uint32:
        ...

    @property
    def timestamp(self) -> Optional[uint64]:
        ...


@streamable
@dataclass(frozen=True)
class BlockRecord(Streamable):
    """
    This class is not included or hashed into the blockchain, but it is kept in memory as a more
    efficient way to maintain data about the blockchain. This allows us to validate future blocks,
    difficulty adjustments, etc, without saving the whole header block in memory.
    """

    header_hash: bytes32
    prev_hash: bytes32  # Header hash of the previous block
    height: uint32
    weight: uint128  # Total cumulative difficulty of all ancestor blocks since genesis
    total_iters: uint128  # Total number of VDF iterations since genesis, including this block
    signage_point_index: uint8
    challenge_vdf_output: ClassgroupElement  # This is the intermediary VDF output at ip_iters in challenge chain
    infused_challenge_vdf_output: Optional[
        ClassgroupElement
    ]  # This is the intermediary VDF output at ip_iters in infused cc, iff deficit <= 3
    reward_infusion_new_challenge: bytes32  # The reward chain infusion output, input to next VDF
    challenge_block_info_hash: bytes32  # Hash of challenge chain data, used to validate end of slots in the future
    sub_slot_iters: uint64  # Current network sub_slot_iters parameter
    required_iters: uint64  # The number of iters required for this proof of space
    deficit: uint8  # A deficit of 16 is an overflow block after an infusion. Deficit of 15 is a challenge block
    overflow: bool
    timestamp: Optional[uint64]

    # Slot (present iff this is the first SB in sub slot)
    finished_challenge_slot_hashes: Optional[List[bytes32]]
    finished_infused_challenge_slot_hashes: Optional[List[bytes32]]
    finished_reward_slot_hashes: Optional[List[bytes32]]

    # Sub-epoch (present iff this is the first SB after sub-epoch)
    sub_epoch_summary_included: Optional[SubEpochSummary]

    @property
    def first_in_sub_slot(self) -> bool:
        return self.finished_challenge_slot_hashes is not None

    def is_challenge_block(self, constants: ConsensusConstants) -> bool:
        return self.deficit == constants.MIN_BLOCKS_PER_CHALLENGE_BLOCK - 1

    def sp_sub_slot_total_iters(self, constants: ConsensusConstants) -> uint128:
        if self.overflow:
            return uint128(self.total_iters - self.ip_iters(constants) - self.sub_slot_iters)
        else:
            return uint128(self.total_iters - self.ip_iters(constants))

    def ip_sub_slot_total_iters(self, constants: ConsensusConstants) -> uint128:
        return uint128(self.total_iters - self.ip_iters(constants))

    def sp_iters(self, constants: ConsensusConstants) -> uint64:
        return calculate_sp_iters(constants, self.sub_slot_iters, self.signage_point_index)

    def ip_iters(self, constants: ConsensusConstants) -> uint64:
        return calculate_ip_iters(
            constants,
            self.sub_slot_iters,
            self.signage_point_index,
            self.required_iters,
        )

    def sp_total_iters(self, constants: ConsensusConstants) -> uint128:
        return uint128(self.sp_sub_slot_total_iters(constants) + self.sp_iters(constants))
