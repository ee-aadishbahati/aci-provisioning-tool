# ACI Provisioning Tool - User Guide

## 🚀 What is the ACI Provisioning Tool?

The ACI Provisioning Tool is a **standalone Windows executable** that automates the provisioning of different configurations directly on ACI fabric and Nexus Dashboard. It's designed to run on machines with **no internet access** - everything is bundled into a single `.exe` file.

## 🎯 What Can It Do?

### Core Capabilities
- **ACI Fabric Provisioning**: Automate tenant, VRF, bridge domain, and EPG creation
- **NDO Multi-Site Management**: Deploy policies across multiple data centers
- **Real API Integration**: Direct REST API calls to APIC and NDO (not dummy implementations)
- **Offline Operation**: Works completely offline with no internet required
- **Configuration Templates**: Pre-built templates for common Essential Energy scenarios
- **Job Tracking**: Monitor provisioning progress with detailed logs
- **Audit Trail**: Complete history of all API calls and changes

### Supported Operations
- **APIC Operations**:
  - Tenant creation and management
  - VRF (Virtual Routing and Forwarding) setup
  - Bridge Domain configuration
  - End Point Group (EPG) provisioning
  - Contract and filter management
  - Application Profile setup

- **NDO Operations**:
  - Schema management across sites
  - Multi-site policy deployment
  - Site association and orchestration
  - Template synchronization

### Essential Energy Integration
- **Site Support**: AUNTH, AUSTH, AUTER data centers
- **Device Types**: OSPI, ESPI, OLFS, ELFS, and other ACI device types
- **Naming Conventions**: Follows Essential Energy standards
- **Node Allocation**: Uses existing toolhub allocation rules

## 📥 How to Download and Install

### Option 1: Download from GitHub Release (Recommended)
1. Go to the GitHub repository: `https://github.com/ee-aadishbahati/aci-provisioning-tool`
2. Click on "Releases" in the right sidebar
3. Download the latest `aci-provisioning-tool.exe` file
4. Copy the `.exe` file to your target machine (no installation required)

### Option 2: Build from Source
If you need to build it yourself:

```bash
# Clone the repository
git clone https://github.com/ee-aadishbahati/aci-provisioning-tool.git
cd aci-provisioning-tool

# Install Python dependencies
pip install -r requirements.txt

# Build the executable
python scripts/build.py

# The executable will be created in dist/aci-provisioning-tool.exe
```

## 🖥️ How to Use the Tool

### Step 1: Start the Application
1. Double-click `aci-provisioning-tool.exe`
2. A command window will appear showing startup messages
3. Your default browser will automatically open to `http://localhost:8080`
4. If the browser doesn't open automatically, manually navigate to `http://localhost:8080`

### Step 2: Configure Connections
1. **APIC Configuration**:
   - Enter APIC IP address or hostname
   - Provide username and password
   - Configure SSL verification settings
   - Test connection to verify credentials

2. **NDO Configuration**:
   - Enter NDO IP address or hostname
   - Provide authentication token or credentials
   - Test connection to verify access

### Step 3: Select Configuration Template
Choose from pre-built templates:
- **Basic ACI Fabric**: Standard tenant/VRF/BD setup
- **Essential Energy IT**: IT-specific fabric configuration
- **Essential Energy OT**: OT-specific fabric configuration
- **Multi-site NDO**: Cross-datacenter deployment
- **Disaster Recovery**: Failover configuration

### Step 4: Customize Configuration
- Modify template parameters (tenant names, VLANs, subnets)
- Set site-specific values (AUNTH, AUSTH, AUTER)
- Configure device assignments and node allocation
- Review configuration before deployment

### Step 5: Execute Provisioning
1. Click "Start Provisioning" to begin
2. Monitor real-time progress in the dashboard
3. View detailed logs for each API call
4. Check for any errors or warnings
5. Review completion summary

### Step 6: Monitor and Audit
- **Job History**: View all previous provisioning jobs
- **Detailed Logs**: Examine API calls and responses
- **Error Analysis**: Troubleshoot any failed operations
- **Export Reports**: Generate audit reports for compliance

## 🏗️ Technical Architecture

### What I Built
- **FastAPI Backend**: Python-based REST API server
- **React Frontend**: Modern web interface with TypeScript
- **SQLite Database**: Local storage for configurations and logs
- **PyInstaller Packaging**: Single-file executable with all dependencies
- **Real API Clients**: Direct integration with APIC and NDO REST APIs

### System Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: 100MB for application + space for logs
- **Network**: Access to APIC and NDO management interfaces
- **Browser**: Chrome, Firefox, or Edge for web interface

### Security Features
- **Local Operation**: Web interface only accessible from localhost
- **Credential Encryption**: All passwords stored securely
- **SSL Support**: Configurable certificate validation
- **Audit Logging**: Complete API call history
- **No Internet Required**: Completely offline operation

## 🔧 Configuration Files

The tool includes several configuration templates:

### Fabric Templates (`templates/fabric_templates.json`)
```json
{
  "basic_fabric": {
    "name": "Basic ACI Fabric",
    "description": "Standard tenant, VRF, and bridge domain setup",
    "tenant": "PROD_TENANT",
    "vrf": "PROD_VRF",
    "bridge_domains": ["WEB_BD", "APP_BD", "DB_BD"]
  }
}
```

### NDO Templates (`templates/ndo_templates.json`)
```json
{
  "multi_site_basic": {
    "name": "Multi-Site Basic",
    "description": "Basic multi-site deployment",
    "sites": ["AUNTH", "AUSTH", "AUTER"],
    "schema": "PROD_SCHEMA"
  }
}
```

## 🚨 Troubleshooting

### Common Issues
1. **Port 8080 Already in Use**:
   - Close other applications using port 8080
   - Or modify the port in the configuration

2. **APIC Connection Failed**:
   - Verify IP address and credentials
   - Check network connectivity
   - Ensure APIC is accessible from your machine

3. **Browser Doesn't Open**:
   - Manually navigate to `http://localhost:8080`
   - Try a different browser
   - Check Windows firewall settings

4. **Executable Won't Start**:
   - Run as Administrator if needed
   - Check antivirus software (may block unsigned executables)
   - Verify Windows version compatibility

### Log Files
- Application logs are stored in the local SQLite database
- Access logs through the web interface under "Job History"
- Export logs for external analysis if needed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the GitHub repository documentation
3. Contact the development team with specific error messages
4. Include log files when reporting issues

---

**Built with**: Python 3.12, FastAPI, React, TypeScript, PyInstaller  
**Version**: 1.0.0  
**Last Updated**: August 2025
