# epik8s-training-lab

This repository is a small EPICS training beamline used to develop and test a simulated and real setup with:

- motor IOCs
- camera IOCs
- Phoebus OPIs
- helper soft IOCs such as `simtwin`, `overlay_rnd`, and `beam_center`
- a single-node Docker Compose deployment generated with `epik8s-compose`

The typical workflow is:

1. clone the repositories
2. install `epik8s-tools`
3. generate the Docker Compose beamline from `beamline_sim.yaml`
4. generate the Phoebus OPI project from `beamline_sim.yaml`
5. start Docker Compose and open Phoebus

## Prerequisites

You need:

- Python 3.10 or newer
- `git`
- `docker` and `docker compose`
- Phoebus installed locally

Optional but useful:

- a Python virtual environment
- Java runtime for Phoebus

## Repositories

The workflow usually uses two repositories side by side:

- `epik8s-tools` for the CLI tools
- `epik8s-training-lab` for the beamline configuration and generated outputs

Example layout:

```text
work/
├── epik8s-tools/
└── epik8s-training-lab/
```

## Install From Scratch

You can install `epik8s-tools` in two ways:

- from the published `pip` package
- from a local clone of the `epik8s-tools` repository

### Option 1: install from pip

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the published package:

```bash
pip install --upgrade pip
pip install epik8s-tools
```

This is the simplest option if you only want to use the commands and you do not need to modify the tool sources.

### Option 2: install from a local clone

Clone the repositories:

```bash
mkdir -p ~/work
cd ~/work

git clone <epik8s-tools-repo-url>
git clone <epik8s-training-lab-repo-url>
```

Create and activate a virtual environment:

```bash
cd ~/work/epik8s-tools
python3 -m venv .venv
source .venv/bin/activate
```

Install the tools from the cloned repository:

```bash
pip install --upgrade pip
pip install -e .
```

Use this option if you are developing or modifying `epik8s-tools` locally.

Verify the commands are available:

```bash
epik8s-compose --help
epik8s-opigen --help
epik8s-run --help
```

## Main Configuration Files

The main beamline configuration files are:

- `beamline.yaml`: main training configuration, including simulated and real components
- `beamline-sim.yaml`: simulation-oriented copy when you want to work only on the simulated setup

These YAML files describe:

- IOC defaults
- services such as notebook and gateways
- IOC instances such as `motorsim`, `camerasim`, `simtwin`, `overlay-rnd`, and `beam_center`
- network and storage settings

## Generate The Docker Compose Beamline

From the training-lab repository root:

```bash
cd ~/work/epik8s-training-lab
source ../epik8s-tools/.venv/bin/activate

epik8s-compose --config beamline_sim.yaml --output test-compose
```

If you want the simulation-only variant, use:

```bash
epik8s-compose --config beamline-sim.yaml --output test-compose
```

This generates a runnable Docker Compose project in `test-compose/`.

Start it with:

```bash
cd test-compose
docker compose up
```

## Generate The Phoebus OPI Project

Generate the OPI project from the same beamline YAML:

```bash
cd ~/work/epik8s-training-lab
source ../epik8s-tools/.venv/bin/activate

epik8s-opigen --config beamline_sim.yaml --projectdir opi
```

This creates or updates the `opi/` directory with:

- `Launcher.bob`: main generated launcher
- `settings.ini`: Phoebus settings for the generated beamline
- `values.yaml`: OPI-side beamline description used by the launcher and helper scripts
- `epik8s-opi/`: reusable OPI widget library used by the generated launcher

If you also want the detailed per-PV launcher and you already generated the compose files with PV lists:

```bash
epik8s-opigen --config beamline_sim.yaml --projectdir opi \
  --detailed --pvlist-dir test-compose/iocs
```

This also generates `Launcher_detailed.bob`.

## Open Phoebus

Once the OPI project exists:

```bash
cd ~/work/epik8s-training-lab/opi
phoebus -settings settings.ini -resource Launcher.bob
```

For the detailed launcher:

```bash
phoebus -settings settings.ini -resource Launcher_detailed.bob
```

## Repository Structure

Top-level directories and files:

- `beamline.yaml`: main beamline definition
- `beamline-sim.yaml`: simulation-only or simulation-focused variant
- `test-compose/`: generated Docker Compose deployment
- `opi/`: generated Phoebus project
- `simtwin/`: soft IOC that links mirror motion to the simulated camera beam position
- `overlay_rnd/`: soft IOC that writes random overlay positions to the camera
- `beam_center/`: soft IOC for closed-loop beam centering on overlay 1
- `docs/`: notes, presentation material, and helper scripts
- `ansible-epics-console-role/`: Ansible role for console setup

## What `test-compose/` Contains

After running `epik8s-compose`, the `test-compose/` directory contains the local runnable beamline.

Important files and directories:

- `docker-compose.yaml`: the generated Docker Compose file
- `epics.env`: shared EPICS network environment used by containers
- `epics-channel.env`: helper environment for host-side CA/PVA client access
- `ports-summary.txt`: summary of exposed ports
- `settings.ini`: Phoebus settings aligned with the generated services
- `iocs/`: per-IOC generated runtime content
- `services/`: service-specific mounted files for gateway-like services
- `notebook-work/`: host directory mounted into the notebook container for persistent notebooks and files
- `examples/pva/`: example Python scripts for PVA access

Inside `test-compose/iocs/` you usually get one directory per IOC, for example:

- `motorsim/`
- `camerasim/`
- `simtwin/`
- `overlay-sim-rnd/`
- `overlay-real-rnd/`
- `beam-center-sim/`

Each IOC directory may contain files such as:

- `beamline.yaml`: IOC-specific rendered configuration
- `config/`: startup scripts, support files, and generated configuration
- `pvlist.txt`: list of PVs exposed by that IOC when available

## What `opi/` Contains

The `opi/` directory is the generated Phoebus project.

Important files:

- `Launcher.bob`: main entry point for operators
- `Launcher_detailed.bob`: optional detailed launcher with PV-level browsing
- `settings.ini`: Phoebus runtime configuration
- `settings_template.ini`: template used for regeneration/customization
- `values.yaml`: beamline description used by dynamic OPI scripts
- `local.ini` and `settings_local.ini`: local overrides for a specific workstation
- `epik8s-opi/`: reusable library of generic OPI panels and Jython scripts

The `epik8s-opi/` subtree contains reusable displays such as:

- motor panels
- camera panels
- vacuum and cooling panels
- helper scripts in `Scripts/`

## What The Custom IOC Directories Contain

- `simtwin/`: simulation logic mapping mirror motor PVs to a synthetic camera beam position
- `overlay_rnd/`: Python soft IOC with a command PV to generate random overlay positions on a camera
- `beam_center/`: Python soft IOC implementing a proportional beam-centering loop using camera centroid and overlay geometry

Each of these directories typically contains:

- a Python program
- `requirements.txt`
- `start.sh` used inside the IOC runtime container

## Typical End-to-End Workflow

```bash
cd ~/work/epik8s-tools
source .venv/bin/activate

cd ~/work/epik8s-training-lab
epik8s-compose --config beamline_sim.yaml --output test-compose
epik8s-opigen --config beamline_sim.yaml --projectdir opi

cd test-compose
docker compose up
```

Then in a second terminal:

```bash
cd ~/work/epik8s-training-lab/opi
phoebus -settings settings.ini -resource Launcher.bob
```

## Notes

- If `epik8s-tools` changes, reinstall it with `pip install -e .` or `pip install .` from the `epik8s-tools` repository.
- The notebook service generated by `epik8s-compose` can expose Jupyter on `http://localhost:8090` if enabled in `beamline_sim.yaml`.
- The generated `test-compose/notebook-work/` directory is the host-side persistent workspace for notebooks.
- Use `test-compose/examples/pva/` as a starting point for Python PVA examples.