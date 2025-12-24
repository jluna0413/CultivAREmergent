# Archon MCP Server Tool Test Report

**Date:** 2025-08-29

**Status:** In Progress


## Tool Test Results

**health_check:**

* **Status:** Success
* **Result:** `{"success": true, "health": {"status": "healthy", "api_service": true, "agents_service": true, "last_health_check": "2025-08-29T23:18:59.557968"}, "uptime_seconds": 5971.2451066970825, "timestamp": "2025-08-29T23:18:59.558060"}`

**session_info:**
* **Status:** Success
* **Result:** `{"success": true, "session_management": {"active_sessions": 0, "session_timeout": 3600, "server_uptime_seconds": 6007.296462774277}, "timestamp": "2025-08-29T23:19:35.609416"}`

**get_available_sources:**
* **Status:** Success
* **Result:** ```json
{
  "success": true,
  "sources": [
    {
      "source_id": "docs.cursor.com",
      "title": "docs.cursor",
      "summary": "Content from docs.cursor.com",
      "metadata": {
        "tags": [
          "cursor"
        ],
        "original_url": "https://docs.cursor.com/en/welcome",
        "auto_generated": true,
        "knowledge_type": "technical",
        "update_frequency": 0
      },
      "total_words": 45069,
      "update_frequency": 7,
      "created_at": "2025-08-26T17:40:36.956002+00:00",
      "updated_at": "2025-08-26T17:40:36.956002+00:00"
    },
    {
      "source_id": "docs.flutter.dev",
      "title": "docs.flutter.dev",
      "summary": "Content from docs.flutter.dev",
      "metadata": {
        "tags": [
          "flutter"
        ],
        "original_url": "https://docs.flutter.dev/",
        "auto_generated": true,
        "knowledge_type": "technical",
        "update_frequency": 0
      },
      "total_words": 994232,
      "update_frequency": 7,
      "created_at": "2025-08-26T17:46:03.346453+00:00",
      "updated_at": "2025-08-26T17:46:03.346453+00:00"
    },
    {
      "source_id": "docs.python.org",
      "title": "docs.python.org",
      "summary": "Content from docs.python.org",
      "metadata": {
        "tags": [],
        "original_url": "https://docs.python.org",
        "auto_generated": true,
        "knowledge_type": "technical",
        "update_frequency": 0
      },
      "total_words": 131987,
      "update_frequency": 7,
      "created_at": "2025-08-26T17:37:00.881025+00:00",
      "updated_at": "2025-08-26T17:37:00.881025+00:00"
    },
    {
      "source_id": "file_Ollama_Starter_Pack_pdf_1756161190",
      "title": "file_Ollama_Starter_Pack_pdf_1756161190",
      "summary": "Content from file_Ollama_Starter_Pack_pdf_1756161190",
      "metadata": {
        "tags": [],
        "auto_generated": true,
        "knowledge_type": "technical",
        "update_frequency": 7
      },
      "total_words": 1583,
      "update_frequency": 7,
      "created_at": "2025-08-25T22:33:15.619892+00:00",
      "updated_at": "2025-08-25T22:33:15.619892+00:00"
    },
    {
      "source_id": "github.com",
      "title": "Archon",
      "summary": "Content from github.com",
      "metadata": {
        "tags": [
          "open-rl"
        ],
        "original_url": "https://github.com/OpenRL-Lab/openrl/tree/main",
        "auto_generated": false,
        "knowledge_type": "technical",
        "update_frequency": 0
      },
      "total_words": 337293,
      "update_frequency": 7,
      "created_at": "2025-08-24T02:02:44.534982+00:00",
      "updated_at": "2025-08-26T17:45:21.925426+00:00"
    },
    {
      "source_id": "jules.google",
      "title": "jules.google",
      "summary": "Content from jules.google",
      "metadata": {
        "tags": [
          "jules",
          "google"
        ],
        "original_url": "https://jules.google/docs/",
        "auto_generated": true,
        "knowledge_type": "technical",
        "update_frequency": 0
      },
      "total_words": 8915,
      "update_frequency": 7,
      "created_at": "2025-08-24T02:15:58.787169+00:00",
      "updated_at": "2025-08-24T02:15:58.787169+00:00"
    }
  ],
  "count": 6
}
```
* **Status:** Success

**perform_rag_query:**
* **Status:** Success
* **Result:** `{"success": true, "results": [], "reranked": false, "error": null}`

**search_code_examples:**
* **Status:** Failure
* **Error:** `{"code":-32001,"data":{"timeout":60000},"name":"McpError","message":"MCP error -32001: Request timed out","stack":"McpError: MCP error -32001: Request timed out\n\tat Timeout.M (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:19559)\n\tat listOnTimeout (node:internal/timers:588:17)\n\tat process.processTimers (node:internal/timers:523:7)"}`

**create_project:**
* **Status:** Success
* **Result:** `{"success": true, "project": {"id": "819fcb71-8910-4ee1-982f-7387cf8b4795", "title": "Archon Tool Test Project", "description": "Project created for testing Archon tools.", "github_repo": null, "created_at": "2025-08-29T23:26:43.93074+00:00", "updated_at": "2025-08-29T23:26:43.930746+00:00", "docs": [], "features": {}, "data": {}, "technical_sources": [], "business_sources": [], "pinned": false}, "project_id": "819fcb71-8910-4ee1-982f-7387cf8b4795", "message": "Project created successfully with ID: 819fcb71-8910-4ee1-982f-7387cf8b4795"}`

**list_projects:**
* **Status:** Failure
* **Error:** `{"code":-32001,"data":{"timeout":60000},"name":"McpError","message":"MCP error -32001: Request timed out","stack":"McpError: MCP error -32001: Request timed out\n\tat Timeout.M (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:19559)\n\tat listOnTimeout (node:internal/timers:588:17)\n\tat process.processTimers (node:internal/timers:523:7)"}`

**get_project:**
* **Status:** Success
* **Result:** `{"success": true, "project": {"id": "819fcb71-8910-4ee1-982f-7387cf8b4795", "title": "Archon Tool Test Project", "description": "Project created for testing Archon tools.", "docs": [], "features": {}, "data": {}, "github_repo": null, "pinned": false, "created_at": "2025-08-29T23:26:43.93074+00:00", "updated_at": "2025-08-29T23:26:43.930746+00:00", "technical_sources": [], "business_sources": []}}`

**delete_project:**
* **Status:** Success
* **Result:** `{"success": true, "message": "Project 819fcb71-8910-4ee1-982f-7387cf8b4795 deleted successfully"}`

**update_project:**
* **Status:** Failure
* **Error:** `{"code":-32000,"name":"McpError","message":"MCP error -32000: Connection closed","stack":"McpError: MCP error -32000: Connection closed\n\tat UNe._onclose (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:15773)\n\tat _transport.onclose (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:15298)\n\tat ChildProcess.<anonymous> (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:828:1591)\n\tat ChildProcess.emit (node:events:518:28)\n\tat EKa.t.emit (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:691:7247)\n\tat abortChildProcess (node:child_process:751:13)\n\tat AbortSignal.onAbortListener (node:child_process:821:7)\n\tat [nodejs.internal.kHybridDispatch] (node:internal/event_target:827:20)\n\tat AbortSignal.dispatchEvent (node:internal/event_target:762:26)\n\tat runAbort (node:internal/abort_controller:486:10)\n\tat abortSignal (node:internal/abort_controller:457:3)\n\tat AbortController.abort (node:internal/abort_controller:505:5)\n\tat YNe.close (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:828:2654)\n\tat eLe.deleteConnection (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:834:1126)\n\tat eLe.updateServerConnections (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:834:2594)\n\tat UEe.<anonymous> (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:833:803)"}`

**create_task:**
* **Status:** Failure
* **Error:** `{"success": false, "error": {"type": "api_error", "message": "Failed to create task: Error creating task: {'message': 'insert or update on table \"archon_tasks\" violates foreign key constraint \"archon_tasks_project_id_fkey\"', 'code': '23503', 'hint': None, 'details': 'Key (project_id)=(819fcb71-8910-4ee1-982f-7387cf8b4795) is not present in table \"archon_projects\".'}", "details": {"response_body": {"detail": {"error": "Error creating task: {'message': 'insert or update on table \"archon_tasks\" violates foreign key constraint \"archon_tasks_project_id_fkey\"', 'code': '23503', 'hint': None, 'details': 'Key (project_id)=(819fcb71-8910-4ee1-982f-7387cf8b4795) is not present in table \"archon_projects\".'}"}}}, "suggestion": "Check that all required parameters are provided and valid", "http_status": 400}`

**list_tasks:**
* **Status:** Failure
* **Error:** `{"code":-32001,"data":{"timeout":60000},"name":"McpError","message":"MCP error -32001: Request timed out","stack":"McpError: MCP error -32001: Request timed out\n\tat Timeout.M (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:19559)\n\tat listOnTimeout (node:internal/timers:588:17)\n\tat process.processTimers (node:internal/timers:523:7)"}`

**get_task:**
* **Status:** Failure
* **Error:** `{"success": false, "error": {"type": "api_error", "message": "Failed to get task: Error getting task: {'message': 'invalid input syntax for type uuid: \"some_task_id\"', 'code': '22P02', 'hint': None, 'details': None}", "details": {"response_body": {"detail": {"error": "Error getting task: {'message': 'invalid input syntax for type uuid: \"some_task_id\"', 'code': '22P02', 'hint': None, 'details': None}"}}}, "suggestion": "Server error. Check server logs for details", "http_status": 500}}`

**update_task:**
* **Status:** Failure
* **Error:** `{"code":-32001,"data":{"timeout":60000},"name":"McpError","message":"MCP error -32001: Request timed out","stack":"McpError: MCP error -32001: Request timed out\n\tat Timeout.M (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:19559)\n\tat listOnTimeout (node:internal/timers:588:17)\n\tat process.processTimers (node:internal/timers:523:7)"}`

**delete_task:**
* **Status:** Failure
* **Error:** `{"code":-32001,"data":{"timeout":60000},"name":"McpError","message":"MCP error -32001: Request timed out","stack":"McpError: MCP error -32001: Request timed out\n\tat Timeout.M (c:\\Users\\jonat\\.vscode\\extensions\\saoudrizwan.claude-dev-3.26.6\\dist\\extension.js:822:19559)\n\tat listOnTimeout (node:internal/timers:588:17)\n\tat process.processTimers (node:internal/timers:523:7)"}`

**search_code_examples:**
* **Status:** Success
* **Result:** `{"success": true, "results": [], "reranked": true, "error": null}`

This section will list the results of testing each Archon tool.  The status will be updated as each tool is tested.
