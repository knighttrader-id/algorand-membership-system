import logging

import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    from smart_contracts.artifacts.membership_system.membership_contract_client import (
        MembershipContractFactory,
        MembershipContractMethodCallCreateParams,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        MembershipContractFactory, default_sender=deployer_.address
    )

    # Explicitly call create_app method during deployment
    # This ensures ApplicationArgs[0] is populated with the method selector
    # so the routing logic can properly match and call create_app
    
    create_params = MembershipContractMethodCallCreateParams(
        method="create_app()void",
        args=None,
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        create_params=create_params,
    )

    logger.info(
        f"Deployed {app_client.app_name} (App ID: {app_client.app_id}) "
        f"at {app_client.app_address}"
    )
    logger.info(f"Operation performed: {result.operation_performed}")

    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        logger.info(f"Funding app account with 1 ALGO...")
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )
        logger.info(f"Successfully funded app account")
