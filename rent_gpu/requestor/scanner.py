import asyncio
from asyncio import TimeoutError
from datetime import datetime, timezone
import pathlib
import sys
from typing import Optional

from sqlmodel import Session, select, delete
from yapapi import props as yp
from yapapi.log import enable_default_logger
from yapapi.props.builder import DemandBuilder
from yapapi.rest import Configuration, Market
from yapapi.rest.market import OfferProposal

from rent_gpu.requestor.db import engine, Offer, OfferStatus

examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


def get_gpu_card(offer: OfferProposal) -> Optional[str]:
    capabilities = offer.props.get("golem.runtime.capabilities", [])
    # Try to detect CUDA card from Norbert's implementation
    cuda_card = next((cap.split(',', 1)[1].strip()
                      for cap in capabilities
                      if cap.startswith('cuda,')),
                     None)

    # Try to detect CUDA card from ITL's implementation
    if cuda_card is None and '!exp:gpu' in capabilities:
        cuda_card = offer.props.get("golem.!exp.gap-35.v1.inf.gpu.model", None)

    return cuda_card


async def list_offers(conf: Configuration, subnet_tag: str):
    async with conf.market() as client:
        market_api = Market(client)
        dbuild = DemandBuilder()
        dbuild.add(yp.NodeInfo(name="Scanner node", subnet_tag=subnet_tag))
        dbuild.add(yp.Activity(expiration=datetime.now(timezone.utc)))
        offers = set()

        with Session(engine) as session:
            stmt = delete(Offer).where(Offer.status == OfferStatus.FREE)
            session.execute(stmt)
            session.commit()

        async with market_api.subscribe(dbuild.properties, dbuild.constraints) as subscription:
            async for event in subscription.events():
                gpu_card = get_gpu_card(event)
                if gpu_card and event.issuer not in offers:
                    offers.add(event.issuer)
                    print(f"Provider: {event.issuer} , Name: {event.props.get('golem.node.id.name')}, Card: {gpu_card}")
                    with Session(engine) as session:
                        existing_offer = session.exec(select(Offer).where(Offer.provider_id == event.issuer)).first()
                        if existing_offer:
                            existing_offer.name = event.props.get('golem.node.id.name')
                            existing_offer.card = gpu_card
                            existing_offer.memory = float(event.props.get('golem.inf.mem.gib'))
                            session.add(existing_offer)
                        else:
                            session.add(
                                Offer(
                                    provider_id=event.issuer,
                                    name=event.props.get('golem.node.id.name'),
                                    card=gpu_card,
                                    memory=float(event.props.get('golem.inf.mem.gib')),
                                )
                            )
                        session.commit()


def main(subnet: str):
    sys.stderr.write(f"Using subnet: {subnet}\n")

    enable_default_logger()
    try:
        asyncio.get_event_loop().run_until_complete(
            asyncio.wait_for(
                list_offers(
                    Configuration(),  # YAGNA_APPKEY will be loaded from env
                    subnet_tag=subnet,
                ),
                timeout=5,
            )
        )
    except TimeoutError:
        pass


if __name__ == "__main__":
    main(sys.argv[1])
