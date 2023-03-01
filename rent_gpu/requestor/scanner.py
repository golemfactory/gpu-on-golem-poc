import asyncio
from asyncio import TimeoutError
from datetime import datetime, timezone
import json
import pathlib
import sys

from yapapi import props as yp
from yapapi.log import enable_default_logger
from yapapi.props.builder import DemandBuilder
from yapapi.rest import Activity, Configuration, Market, Payment  # noqa

examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


async def list_offers(conf: Configuration, subnet_tag: str):
    async with conf.market() as client:
        market_api = Market(client)
        dbuild = DemandBuilder()
        dbuild.add(yp.NodeInfo(name="Scanner node", subnet_tag=subnet_tag))
        dbuild.add(yp.Activity(expiration=datetime.now(timezone.utc)))
        offers = set()

        async with market_api.subscribe(dbuild.properties, dbuild.constraints) as subscription:
            async for event in subscription.events():
                capabilities = event.props.get("golem.runtime.capabilities", [])
                cuda_card = next((cap.split(',', 1)[1].strip()
                                  for cap in capabilities
                                  if cap.startswith('cuda,')),
                                 None)
                if cuda_card and event.issuer not in offers:
                    offers.add(event.issuer)
                    print(f"Provider: {event.issuer}, Name: {event.props.get('golem.node.id.name')}, Card: {cuda_card}")
                    # print(f"props {json.dumps(event.props, indent=4)}")
        print("done")


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
