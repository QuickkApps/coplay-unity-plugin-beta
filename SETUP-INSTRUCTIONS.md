# Coplay GLM Proxy - Complete Setup Guide

## ⚠️ IMPORTANT: Separate from Unity Package

The GLM proxy server should **NOT** be installed inside the Unity package folder. It runs as a separate application on your computer.

## 📁 What Happened

I moved all proxy files to a separate `coplay-glm-proxy/` folder outside the Unity package structure. This prevents Unity from trying to manage the Python files.

## 🚀 Quick Setup (5 minutes)

### Step 1: Navigate to Proxy Folder
```bash
cd coplay-glm-proxy
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start the Proxy Server
**Windows:**
```bash
start-proxy.bat
```

**macOS/Linux:**
```bash
chmod +x start-proxy.sh
./start-proxy.sh
```

**Or manually:**
```bash
python coplay-glm-proxy.py
```

### Step 4: Configure Coplay in Unity

1. Open Unity and launch Coplay (`Ctrl+G` or Window → Coplay)
2. Click **Settings** button (⚙️)
3. Configure these settings:
   - **API Provider**: "OpenAI Compatible"
   - **OpenAI Base URL**: `http://localhost:8080/v1`
   - **API Key**: `df92b900aac94a60b659c341d9054464.PkbniOA3fCgPCtlu`
   - **Model Name**: `glm-4.6`

4. Click **Save**

### Step 5: Test It
Send a message like: "Create a simple Unity C# script"

You should see activity in the proxy server window showing the requests being processed.

## 🔧 Troubleshooting

### If Unity Shows Meta File Errors:
- ✅ **Fixed!** Files are now in separate folder
- Delete any remaining `__pycache__` folders
- Unity may need to refresh (Assets → Refresh)

### If Connection Fails:
1. Make sure proxy server is running (you see "Proxy server running on http://localhost:8080")
2. Check firewall isn't blocking port 8080
3. Verify URL in Coplay settings: `http://localhost:8080/v1`

### Test the Proxy:
```bash
cd coplay-glm-proxy
python test-proxy.py
```

## 📁 File Structure
```
coplay-unity-plugin-beta/
├── Editor/                    # Unity package files
├── package.json              # Unity package manifest
├── README.md                 # Coplay documentation
├── SETUP-INSTRUCTIONS.md     # This file
└── coplay-glm-proxy/         # 🚨 Separate proxy application
    ├── coplay-glm-proxy.py   # Main proxy server
    ├── requirements.txt       # Python dependencies
    ├── start-proxy.bat       # Windows launcher
    ├── start-proxy.sh        # macOS/Linux launcher
    ├── test-proxy.py         # Test script
    └── README-GLM-Setup.md  # Detailed documentation
```

## 🔄 Daily Usage

1. **Start Proxy:** Run `start-proxy.bat` (Windows) or `./start-proxy.sh` (macOS/Linux)
2. **Open Unity:** Launch your project
3. **Use Coplay:** Works normally with your GLM API
4. **Stop Proxy:** Press `Ctrl+C` in proxy window

## 💡 Pro Tips

- **Background:** Use `pythonw.exe coplay-glm-proxy.py` on Windows to run without terminal
- **Auto-start:** Add the proxy script to your system's startup applications
- **Port Change:** Edit `PROXY_PORT = 8080` in the Python script if needed
- **Monitoring:** Watch the proxy logs to see API activity and debug issues

## 🔐 Security Notes

- Proxy runs locally only (localhost)
- Your GLM API key is embedded in the proxy
- No data sent to third parties beyond GLM API
- Proxy logs contain your chat content

## 🎯 Done!

You can now use Coplay with your GLM coding plan instead of the paid subscription. The proxy handles all the API translation automatically.

All Coplay features work:
- ✅ Code generation and debugging
- ✅ Unity asset management  
- ✅ Pipeline recording and replay
- ✅ Context-aware assistance
- ✅ Function calling

Enjoy your free Coplay experience with GLM! 🎉
