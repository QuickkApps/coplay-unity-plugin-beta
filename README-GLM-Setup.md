# Coplay GLM Proxy Setup Guide

This guide will help you set up Coplay to use your GLM coding plan API instead of the paid subscription.

## What This Does

The proxy server sits between Coplay and your GLM API, translating requests and responses so Coplay can use your GLM API key seamlessly.

## Prerequisites

- Python 3.7 or higher
- Your GLM API credentials (already configured in the proxy)
- Coplay Unity plugin installed

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Proxy Server

```bash
python coplay-glm-proxy.py
```

You should see output like:
```
2025-10-26 03:58:00 - INFO - Starting Coplay GLM Proxy Server...
2025-10-26 03:58:00 - INFO - GLM API URL: https://api.z.ai/api/coding/paas/v4
2025-10-26 03:58:00 - INFO - Default Model: glm-4.6
2025-10-26 03:58:00 - INFO - Proxy Port: 8080
2025-10-26 03:58:00 - INFO - Proxy server running on http://localhost:8080
```

### 3. Configure Coplay

1. Open Unity and launch Coplay (Window → Coplay → Toggle Window or `Ctrl+G`)

2. Click the **Settings** button (gear icon ⚙️) in the top-right

3. In the Settings panel, configure the following:
   - **API Provider**: Select "OpenAI Compatible"
   - **OpenAI Base URL**: `http://localhost:8080/v1`
   - **API Key**: `df92b900aac94a60b659c341d9054464.PkbniOA3fCgPCtlu`
   - **Model Name**: `glm-4.6`

4. Save the settings

### 4. Test the Configuration

1. Try sending a simple message like "Hello, can you help me create a Unity script?"
2. You should see log output in the proxy server terminal showing the requests
3. If successful, Coplay will respond using your GLM API instead of the paid service

## Advanced Configuration

### Changing the Proxy Port

If port 8080 is already in use, you can change it:

1. Edit `coplay-glm-proxy.py`
2. Change `PROXY_PORT = 8080` to your desired port
3. Update your Coplay Base URL to match (e.g., `http://localhost:3000/v1`)

### Running as Background Service

#### Windows:
```bash
pythonw.exe coplay-glm-proxy.py
```

#### macOS/Linux:
```bash
nohup python coplay-glm-proxy.py > proxy.log 2>&1 &
```

### Checking Proxy Status

You can check if the proxy is running by visiting:
```
http://localhost:8080/health
```

## Troubleshooting

### Connection Refused
- Make sure the proxy server is running
- Check that the port isn't blocked by firewall
- Verify the URL in Coplay settings matches the proxy port

### Authentication Errors
- Verify your GLM API key is correct
- Check that the GLM API endpoint is accessible
- Look at the proxy logs for detailed error messages

### Slow Response Times
- The proxy adds minimal overhead
- Check your internet connection to the GLM API
- Monitor the proxy logs for any repeated requests

### Feature Limitations

Some advanced Coplay features might not work perfectly:
- Function calling may need additional translation
- Image context handling might need updates
- Pipeline recording should work normally

## Security Notes

- The proxy runs locally on your machine only
- Your GLM API key is embedded in the proxy script
- Consider who has access to the proxy files
- The proxy logs contain your chat content

## Log Files

The proxy server outputs detailed logs including:
- Incoming requests from Coplay
- Translated requests to GLM API
- GLM API responses
- Any errors that occur

Use these logs to debug issues or monitor usage.

## Stopping the Proxy

Press `Ctrl+C` in the terminal where the proxy is running, or close the terminal window.

## Next Steps

Once configured, you can use Coplay normally with all features:
- Code generation and debugging
- Unity asset management
- Pipeline recording and replay
- Context-aware assistance

All requests will now go through your GLM API instead of the paid Coplay service.
