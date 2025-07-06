from fastmcp import FastMCP
from anki_mcp_server.anki_connect import make_anki_request
from anki_mcp_server.models.models import ModelList, ModelDetails, ErrorResponse


async def list_models() -> ModelList | ErrorResponse:
    """Get the names of all note models from Anki"""
    try:
        models = await make_anki_request("modelNames")
        return ModelList(models=models)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="retrieving models")


async def get_model(model_name: str) -> ModelDetails | ErrorResponse:
    """Get a model, including field and template definitions, from Anki"""
    try:
        models = await make_anki_request(
            "findModelsByName", {"modelNames": [model_name]}
        )
        return ModelDetails(model_name=model_name, details=models)
    except Exception as e:
        return ErrorResponse(error=str(e), operation=f"retrieving model '{model_name}'")


def register_models_tools(mcp: FastMCP):
    mcp.tool(list_models)
    mcp.tool(get_model)
