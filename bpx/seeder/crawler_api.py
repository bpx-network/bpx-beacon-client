from __future__ import annotations

from typing import Optional

from bpx.protocols import beacon_protocol, wallet_protocol
from bpx.seeder.crawler import Crawler
from bpx.server.outbound_message import Message
from bpx.server.server import ChiaServer
from bpx.server.ws_connection import WSChiaConnection
from bpx.util.api_decorators import api_request


class CrawlerAPI:
    crawler: Crawler

    def __init__(self, crawler):
        self.crawler = crawler

    def __getattr__(self, attr_name: str):
        async def invoke(*args, **kwargs):
            pass

        return invoke

    @property
    def server(self) -> ChiaServer:
        assert self.crawler.server is not None
        return self.crawler.server

    @property
    def log(self):
        return self.crawler.log

    @api_request(peer_required=True)
    async def request_peers(self, _request: beacon_protocol.RequestPeers, peer: WSChiaConnection):
        pass

    @api_request(peer_required=True)
    async def respond_peers(
        self, request: beacon_protocol.RespondPeers, peer: WSChiaConnection
    ) -> Optional[Message]:
        pass

    @api_request(peer_required=True)
    async def new_peak(self, request: beacon_protocol.NewPeak, peer: WSChiaConnection) -> Optional[Message]:
        await self.crawler.new_peak(request, peer)
        return None

    @api_request()
    async def new_transaction(self, transaction: beacon_protocol.NewTransaction) -> Optional[Message]:
        pass

    @api_request(peer_required=True)
    async def new_signage_point_or_end_of_sub_slot(
        self, new_sp: beacon_protocol.NewSignagePointOrEndOfSubSlot, peer: WSChiaConnection
    ) -> Optional[Message]:
        pass

    @api_request()
    async def new_unfinished_block(
        self, new_unfinished_block: beacon_protocol.NewUnfinishedBlock
    ) -> Optional[Message]:
        pass

    @api_request(peer_required=True)
    async def new_compact_vdf(self, request: beacon_protocol.NewCompactVDF, peer: WSChiaConnection):
        pass

    @api_request()
    async def request_transaction(self, request: beacon_protocol.RequestTransaction) -> Optional[Message]:
        pass

    @api_request()
    async def request_proof_of_weight(self, request: beacon_protocol.RequestProofOfWeight) -> Optional[Message]:
        pass

    @api_request()
    async def request_block(self, request: beacon_protocol.RequestBlock) -> Optional[Message]:
        pass

    @api_request()
    async def request_blocks(self, request: beacon_protocol.RequestBlocks) -> Optional[Message]:
        pass

    @api_request()
    async def request_unfinished_block(
        self, request_unfinished_block: beacon_protocol.RequestUnfinishedBlock
    ) -> Optional[Message]:
        pass

    @api_request()
    async def request_signage_point_or_end_of_sub_slot(
        self, request: beacon_protocol.RequestSignagePointOrEndOfSubSlot
    ) -> Optional[Message]:
        pass

    @api_request(peer_required=True)
    async def request_mempool_transactions(
        self,
        request: beacon_protocol.RequestMempoolTransactions,
        peer: WSChiaConnection,
    ) -> Optional[Message]:
        pass

    @api_request()
    async def request_block_header(self, request: wallet_protocol.RequestBlockHeader) -> Optional[Message]:
        pass

    @api_request()
    async def request_additions(self, request: wallet_protocol.RequestAdditions) -> Optional[Message]:
        pass

    @api_request()
    async def request_removals(self, request: wallet_protocol.RequestRemovals) -> Optional[Message]:
        pass

    @api_request()
    async def request_puzzle_solution(self, request: wallet_protocol.RequestPuzzleSolution) -> Optional[Message]:
        pass

    @api_request()
    async def request_header_blocks(self, request: wallet_protocol.RequestHeaderBlocks) -> Optional[Message]:
        pass
