import subprocess
import json
import os

# The MCP configuration file is expected to be in the project directory.
# However, the memory server itself is configured to store data in a global location.
MCP_CONFIG_PATH = "/home/shayne/agent-zero/usr/projects/agent_zero_enhancements_and_extensions/mcp.json"
MEMORY_SERVER_NAME = "memory"
GLOBAL_MEMORY_FILE = "/home/shayne/agent-zero/memory.jsonl"

def _call_mcpl_memory(tool_name, arguments):
    """
    Internal helper to call the MCP memory server using mcpl.
    """
    if not os.path.exists(MCP_CONFIG_PATH):
        return {"error": "MCP config not found. Please configure MCP first."}

    cmd = ["mcpl", "call", MEMORY_SERVER_NAME, tool_name, json.dumps(arguments)]
    
    # Ensure PATH includes mcpl
    env = os.environ.copy()
    env["PATH"] = "/root/.local/bin:" + env.get("PATH", "")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
        
        if result.returncode != 0:
            return {"error": result.stderr}
            
        # Parse the JSON output from mcpl
        try:
            output_data = json.loads(result.stdout)
            # mcpl wraps the actual result in a "result" string sometimes
            if "result" in output_data and isinstance(output_data["result"], str):
                return json.loads(output_data["result"])
            return output_data
        except json.JSONDecodeError:
            return {"raw_output": result.stdout}
            
    except FileNotFoundError:
        return {"error": "mcpl command not found. Please install MCP Launchpad."}
    except subprocess.TimeoutExpired:
        return {"error": "MCP server timeout"}
    except Exception as e:
        return {"error": str(e)}

def _sanitize_entity(entity):
    """
    Sanitize entity data to match MCP memory schema.
    Removes fields like 'type' that cause schema validation errors.
    """
    if not isinstance(entity, dict):
        return entity
    
    # Only keep allowed fields according to schema
    allowed_fields = {'name', 'entityType', 'observations'}
    sanitized = {}
    
    for key, value in entity.items():
        if key in allowed_fields:
            sanitized[key] = value
    
    return sanitized

def search_memory(query):
    """
    Search the memory graph for entities, relations, and observations matching the query.
    """
    result = _call_mcpl_memory("search_nodes", {"query": query})
    
    # Sanitize entities to remove schema-invalid fields
    if "entities" in result:
        result["entities"] = [_sanitize_entity(e) for e in result["entities"]]
    
    return result

def get_related_entities(entity_name):
    """
    Get the entity details and its relations.
    """
    result = _call_mcpl_memory("open_nodes", {"names": [entity_name]})
    
    # Sanitize entities
    if "entities" in result:
        result["entities"] = [_sanitize_entity(e) for e in result["entities"]]
    
    return result

def add_memory(entity_name, observations):
    """
    Add observations to an existing entity.
    Creates the entity if it doesn't exist.
    """
    # First, try to add observations. If entity doesn't exist, create it.
    result = _call_mcpl_memory("add_observations", {
        "observations": [{
            "entityName": entity_name,
            "contents": observations if isinstance(observations, list) else [observations]
        }]
    })
    
    if "error" in result and "not found" in result.get("error", "").lower():
        # Entity likely doesn't exist, create it
        create_result = _call_mcpl_memory("create_entities", {
            "entities": [{
                "name": entity_name,
                "entityType": "general",
                "observations": observations if isinstance(observations, list) else [observations]
            }]
        })
        return create_result
        
    return result

def read_full_graph():
    """
    Read the entire knowledge graph.
    """
    # Note: read_graph might fail due to schema validation in mcpl,
    # but we can try. If it fails, we rely on search.
    result = _call_mcpl_memory("read_graph", {})
    
    # Sanitize entities
    if "entities" in result:
        result["entities"] = [_sanitize_entity(e) for e in result["entities"]]
    
    return result

def get_context_for_project(project_name):
    """
    Retrieve relevant memory context for a specific project or task.
    """
    # Search for project name and general capabilities
    results = search_memory(project_name)
    
    # If no specific results, return general system knowledge
    if not results or ("entities" in results and len(results["entities"]) == 0):
        return search_memory("Agent Zero")
        
    return results

if __name__ == "__main__":
    # Test the module
    print("Testing MCP Memory Integration...")
    print("Searching for 'Agent Zero':")
    print(search_memory("Agent Zero"))
