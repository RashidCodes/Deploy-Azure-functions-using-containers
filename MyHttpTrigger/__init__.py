import logging
import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:

    keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    secretName = req.params.get("secretName")

    if secretName is None:
        return HttpResponse(
            json.dumps({
                "message": "Provide a secret name"
            }),
            mimetype="application/json"
        )

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    retrieved_secret = client.get_secret(secretName)

    return HttpResponse(
        json.dumps({
            "secret": retrieved_secret.value
        }),
        mimetype="application/json"
    )
