# ACI Provisioning Tool

A standalone Windows executable for automated ACI fabric and Nexus Dashboard Orchestrator (NDO) provisioning. This tool operates completely offline and provides real REST API integration with APIC and NDO systems.

## Overview

This tool automates the provisioning of different configurations directly on ACI fabric and Nexus Dashboard. It's designed to run on machines with no internet access as a single `.exe` file that can be double-clicked to start.

## Features

- **Standalone Operation**: Single `.exe` file with no external dependencies
- **Real API Integration**: Actual APIC and NDO REST API calls (not dummy implementations)
- **Template-Based Configuration**: Pre-built templates for common ACI deployments
- **Progress Tracking**: Real-time monitoring of provisioning tasks
- **Audit Logging**: Complete audit trail of all API operations
- **Multi-Site Support**: NDO orchestration across multiple data centers
- **Essential Energy Integration**: Leverages existing naming conventions and node allocation rules

## Architecture

- **Backend**: Python 3.12 + FastAPI with embedded web server
- **Frontend**: React + TypeScript with Tailwind CSS
- **Database**: SQLite for configuration templates and logs
- **Packaging**: PyInstaller for single-file Windows executable
- **API Clients**: Custom APIC and NDO REST clients with authentication

## Quick Start

### For End Users

1. Download the `aci-provisioning-tool.exe` file
2. Double-click to start the application
3. The tool will open in your default web browser at `http://localhost:8080`
4. Configure your APIC/NDO credentials and start provisioning

### For Developers

#### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/ee-aadishbahati/aci-provisioning-tool.git
cd aci-provisioning-tool

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Start development servers
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend (in another terminal)
cd frontend
npm run dev
```

#### Building the Executable

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Build executable
python scripts/build.py

# Package for distribution
python scripts/package.py
```

## Project Structure

```
aci-provisioning-tool/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── build.spec                       # PyInstaller configuration
├── 
├── backend/                         # FastAPI backend
│   ├── main.py                      # FastAPI application
│   ├── models/                      # Data models
│   │   ├── aci_models.py           # ACI configuration models
│   │   ├── ndo_models.py           # NDO configuration models
│   │   └── database.py             # Database models
│   ├── clients/                     # API clients
│   │   ├── apic_client.py          # APIC REST client
│   │   └── ndo_client.py           # NDO REST client
│   ├── services/                    # Business logic
│   │   └── provisioning.py        # Core provisioning service
│   └── routes/                      # API endpoints
│       ├── provisioning.py        # Provisioning endpoints
│       └── status.py               # Status endpoints
│
├── frontend/                        # React frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── services/               # API service layer
│   │   ├── types/                  # TypeScript definitions
│   │   └── hooks/                  # Custom React hooks
│   ├── package.json
│   └── dist/                       # Built frontend (embedded)
│
├── templates/                       # Configuration templates
│   ├── fabric_templates.json      # ACI fabric configurations
│   └── ndo_templates.json         # NDO policy templates
│
└── scripts/                        # Build and packaging scripts
    ├── build.py                    # Build automation
    └── package.py                 # Distribution packaging
```

## Configuration Templates

The tool includes pre-built templates for common scenarios:

### ACI Fabric Templates
- **Basic ACI Fabric**: Standard configuration with common tenants
- **Essential Energy IT**: IT fabric for Essential Energy data centers
- **Essential Energy OT**: OT fabric with SCADA integration

### NDO Templates
- **Multi-Site Basic**: Basic multi-site schema
- **Essential Energy Multi-Site**: EE-specific multi-site configuration
- **Disaster Recovery**: DR configuration with site failover

## API Integration

### APIC REST API
- Cookie-based authentication
- Tenant, VRF, and Bridge Domain management
- Application Profile and EPG provisioning
- Fabric node discovery

### NDO REST API
- Token-based authentication
- Schema and template management
- Multi-site deployment orchestration
- Deployment status monitoring

## Security

- **Local Operation**: Web interface bound to localhost only
- **Credential Encryption**: All credentials encrypted locally
- **SSL/TLS**: HTTPS communication with APIC/NDO
- **Audit Logging**: Complete API call audit trail
- **No External Dependencies**: Fully self-contained operation

## Essential Energy Integration

This tool leverages existing Essential Energy infrastructure:

- **Site Codes**: AUNTH, AUSTH, AUTER data centers
- **Device Types**: ACI device types (OSPI, ESPI, OLFS, ELFS, etc.)
- **Node Allocation**: Automated node ID allocation per site and environment
- **Naming Conventions**: Consistent with existing toolhub patterns

## Development

### Adding New Templates

1. Edit `templates/fabric_templates.json` or `templates/ndo_templates.json`
2. Follow the existing schema structure
3. Test with validation endpoint: `POST /api/provisioning/validate-config`

### Extending API Clients

1. Add new methods to `backend/clients/apic_client.py` or `ndo_client.py`
2. Update corresponding models in `backend/models/`
3. Add service layer logic in `backend/services/provisioning.py`
4. Create API endpoints in `backend/routes/`

### Frontend Development

1. Add new components in `frontend/src/components/`
2. Update types in `frontend/src/types/index.ts`
3. Extend API service in `frontend/src/services/api.ts`
4. Follow existing patterns for state management and error handling

## Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
python -m pytest tests/integration/

# Build test
python scripts/build.py
```

## Deployment

The tool is designed for offline deployment:

1. Build the executable using `scripts/build.py`
2. Package using `scripts/package.py`
3. Distribute the resulting ZIP file
4. Users extract and run `aci-provisioning-tool.exe`

## Support

For technical support or questions:
- **Primary Contact**: aadish.bahati@essentialenergy.com.au
- **Repository**: https://github.com/ee-aadishbahati/aci-provisioning-tool

## License

Copyright © 2025 Essential Energy. All rights reserved.

---

**Note**: This tool is designed for Essential Energy's specific ACI deployment requirements and integrates with existing infrastructure patterns from the ACI Deployment Tracker and Toolhub platforms.
