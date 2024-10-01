"""
Definition of Synchronous and Asynchronous version of a
helper functions to access to the REST API of Ensembl.
"""

import sys
import asyncio
import requests


# A few hand JSON types (from ArjanCode Python Next Level Course)
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


# Define some helper functions
# Synchronous version of fetch_endpoint()
def fetch_endpoint_sync(base_url: str, endpoint: str, content_type: str) -> JSONObject:
    """
    Synchronous version of a helper function to fetch data from Ensembl REST API.
    """

    response = requests.get(base_url+endpoint, headers={ "Content-Type" : content_type})

    if not response.ok:
        response.raise_for_status()
        sys.exit()

    if content_type == 'application/json':
        return response.json()
    else:
        return response.text


# Asynchronous version of fetch_endpoint()
async def fetch_endpoint(base_url: str, endpoint: str, content_type: str) -> JSONObject:
    """
    Asynchronous version of the helper function to fetch data from Ensembl REST API.
    """
    return await asyncio.to_thread(fetch_endpoint_sync, base_url, endpoint, content_type)


# Can we compare with POST queries (they are bulk REST API calls)?
# POST version of fetch_endpoint_sync()
def fetch_endpoint_POST(base_url: str, endpoint: str, data: JSONObject, content_type: str) -> JSONObject:

    responses = requests.post(
                              base_url+endpoint, 
                              headers={ "Accept" : content_type, "Content-Type" : content_type}, 
                              data=data
                              )

    if not responses.ok:
        responses.raise_for_status()
        sys.exit()

    if content_type == 'application/json':
        return responses.json()
    else:
        return responses.text

