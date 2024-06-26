import asyncio
from asyncio import TimeoutError
from datetime import datetime, timezone
import pathlib
import sys

from sqlmodel import Session, select, delete
from yapapi import props as yp
from yapapi.log import enable_default_logger
from yapapi.props.builder import DemandBuilder
from yapapi.rest import Configuration, Market
from yapapi.rest.market import OfferProposal

from rent_gpu.requestor.db import engine, Offer, OfferStatus

examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


def has_vm_nvidia_runtime(offer: OfferProposal) -> bool:
    capabilities = offer.props.get("golem.runtime.capabilities", [])
    return offer.props.get("golem.runtime.name", '') == 'vm-nvidia' and '!exp:gpu' in capabilities


def delete_current_offers():
    with Session(engine) as session:
        stmt = delete(Offer).where(Offer.status == OfferStatus.FREE)
        session.execute(stmt)
        session.commit()


def create_offer_from_proposal(event: OfferProposal):
    gpu_card = event.props.get("golem.!exp.gap-35.v1.inf.gpu.model", None)
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


async def list_offers(conf: Configuration, subnet_tag: str):
    async with conf.market() as client:
        market_api = Market(client)
        dbuild = DemandBuilder()
        dbuild.add(yp.NodeInfo(name="Scanner node", subnet_tag=subnet_tag))
        dbuild.add(yp.Activity(expiration=datetime.now(timezone.utc)))

        delete_current_offers()

        offers = set()
        async with market_api.subscribe(dbuild.properties, dbuild.constraints) as subscription:
            async for event in subscription.events():
                if has_vm_nvidia_runtime(event) and event.issuer not in offers:
                    offers.add(event.issuer)
                    gpu_card = event.props.get("golem.!exp.gap-35.v1.inf.gpu.model", None)
                    create_offer_from_proposal(event)
                    print(f"Provider: {event.issuer} , Name: {event.props.get('golem.node.id.name')}, Card: {gpu_card}")


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
