# Smart Server Monitoring and Automation System

A Linux desktop application for monitoring system resources, visualizing
live performance data, recording events, and notifying the user when
configured resource thresholds are exceeded.

> **Project status:** The core monitoring application and graphical
> dashboard are implemented. The optional AI assistant is experimental
> and is not required to run the monitoring system.

## Table of contents

-   [Overview](#overview)
-   [Main features](#main-features)
-   [Technology stack](#technology-stack)
-   [How the application works](#how-the-application-works)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Launch the application](#launch-the-application)
-   [Generated files](#generated-files)
-   [Alerts and monitoring behaviour](#alerts-and-monitoring-behaviour)
-   [Optional network protection](#optional-network-protection)
-   [AI assistant status](#ai-assistant-status)
-   [Troubleshooting](#troubleshooting)
-   [Project structure](#project-structure)

## Overview

Smart Server Monitoring and Automation System is a Python-based Linux
monitoring application. It collects system-performance information,
displays it in a desktop dashboard, and records monitoring events so
that the user can review them.

The application is designed to make important system information easier
to understand through a graphical interface rather than relying only on
terminal output.

## Main features

### System resource monitoring

-   CPU usage.
-   RAM usage.
-   Disk usage and disk activity.
-   Network activity, including download information.
-   Per-core CPU load.
-   System load and other system statistics exposed by the dashboard.

### Graphical dashboard

The desktop interface is built with HTML, CSS and JavaScript and
displayed in a native application window using PyWebView. It presents
live readings and charts for the monitored resources.

The dashboard is opened automatically when the user starts `client.py`.
The user does not need to open the generated HTML page manually.

### Threshold-based alerts

The monitoring logic classifies resource usage into configured states
such as **Normal**, **Warning** and **Critical**. When configured
conditions are met, the application can send desktop notifications.

Examples of implemented alert logic include: - CPU usage thresholds,
including sustained high usage. - RAM high-usage episodes and a
notification after repeated episodes. - Disk usage warnings and a
critical notification when very high usage persists.

The exact thresholds and timing are defined in the Python monitoring
logic and may be adjusted in the source code.

### Event logging and search

-   Monitoring events are appended to `monitor.log`.
-   Current resource readings are written to `monitor_data.json`.
-   The application includes log-search functionality to find entries
    containing a chosen keyword.
-   The dashboard includes monitoring controls such as pause/resume
    where provided by the current interface.

## Technology stack

  Technology          Purpose
  ------------------- --------------------------------------------------
  Python              Monitoring logic and application control
  psutil              Reading CPU, memory, disk and network statistics
  HTML / CSS          Dashboard structure and styling
  JavaScript          Dashboard charts and interactive elements
  PyWebView           Displaying the dashboard in a desktop window
  Qt / PyQt6          Desktop rendering backend for PyWebView
  notify-send         Linux desktop notifications
  FastAPI             Optional remote AI service API
  Google Gemini API   Experimental AI assistant integration

## How the application works

1.  The user launches `client.py` from the project directory.
2.  Python starts the local monitoring service and the monitoring loop.
3.  The application collects system statistics using `psutil`.
4.  The dashboard displays the readings and charts in a desktop window.
5.  Monitoring events are written to the log file and current readings
    are saved to the data file.
6.  When configured alert conditions are met, the application sends a
    desktop notification.

The dashboard is served locally by the application. In the current
configuration, its local address is `http://127.0.0.1:8766/`.

## Requirements

-   Ubuntu or another compatible Linux distribution.
-   Python 3.
-   `pip` and Python virtual-environment support.
-   A graphical desktop session to display the PyWebView window and
    desktop notifications.

Some system-monitoring or network-protection operations use Linux
command-line utilities such as `top`, `free`, `df`, `ss`, `notify-send`
and, optionally, UFW.

## Installation

### 1. Install system packages

On Ubuntu, open Terminal and run:

``` bash
sudo apt update
sudo apt install python3 python3-venv python3-pip libnotify-bin
```

UFW is only needed if you intend to use the optional
firewall/IP-blocking functionality:

``` bash
sudo apt install ufw
```

Do not enable or change firewall rules unless you understand the effect
on your machine and network.

### 2. Download the project

Download the project ZIP from its GitHub repository and extract it, or
clone the repository:

``` bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with the actual repository URL and extracted
folder name.

### 3. Create and activate a virtual environment

Run these commands from the project directory:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the project's Python dependencies

The project already has a `requirements.txt` file listing its Python
dependencies. Install them from that file rather than typing the package
names again:

``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run this command from the project directory, with the virtual environment
activated. If a dependency is missing from `requirements.txt`, add it to
that file and reinstall. This keeps `requirements.txt` as the single
source of truth for the project's dependencies.

## Launch the application

Make sure the virtual environment is activated and that the Terminal is
in the project directory.

Run:

``` bash
python client.py
```

The application should start the monitoring process and open the
**System Monitor** desktop window automatically.

**Important:** The main client file is named `client.py`. It was
previously named `script3.py`; use the new filename when launching the
application.

Do not try to run `monitor_gui.html` directly. The application
creates/serves the dashboard as part of its startup process.

### Stop the application

Use `Ctrl + C` in the Terminal where the application was launched. If
the window is still open, close it and then stop the running process
from that Terminal.

## Generated files

The application creates or updates the following files while it runs:

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `monitor.log`                       Recorded monitoring events and
                                      resource statuses

  `monitor_data.json`                 Latest CPU, RAM and disk readings
                                      used by the application

  `monitor_gui.html`                  Dashboard HTML generated by the
                                      client at startup, if generated by
                                      the current version
  -----------------------------------------------------------------------

These are runtime files. If they are not present before the first
launch, that can be normal; the application may create them when it
starts.

## Alerts and monitoring behaviour

The monitoring logic uses configured thresholds to distinguish normal,
warning and high/critical resource usage. Some alerts depend not only on
the measured percentage but also on how long the condition continues or
how many high-usage episodes occur.

The application can display desktop notifications through Linux
`notify-send`. Notifications require a working graphical desktop
notification service.

Thresholds and alert timing should be checked in `client.py` before
being described as fixed specifications in external documentation.

## Optional network protection

The project includes code for checking network connections and, where
configured, attempting to block explicitly listed IP addresses through
UFW.

This is an optional system-level operation: - UFW must be installed and
active. - The application must have the required permissions to add
firewall rules. - Only IP addresses explicitly configured for this
purpose should be considered for blocking. - A network connection by
itself does not prove that an IP address is malicious.

Use firewall functionality carefully. Incorrect rules can interrupt
legitimate network access.

## AI assistant status

The project has an experimental AI assistant integration that
communicates with a separately hosted FastAPI service and a Gemini
model.

**The AI assistant is currently experimental and may be unavailable**,
for example because of API quota limits, service configuration, network
connectivity or hosting issues. It should not be considered a fully
reliable core feature.

-   The AI assistant is not required for CPU, RAM, disk or network
    monitoring.
-   End users should not place private API keys in the desktop client or
    commit keys to GitHub.
-   Any provider API key must be stored as a secret in the backend
    hosting environment.
-   The AI assistant does not perform automatic predictive analysis of
    future system failures.

The monitoring dashboard and logging functions should be evaluated
independently of the experimental AI feature.

## Troubleshooting

### The desktop window does not open

-   Confirm that you are using a graphical Linux desktop session.
-   Activate the virtual environment.
-   Confirm that PyWebView and the Qt/PyQt6 dependencies are installed.
-   Read any error displayed in the Terminal.

### `ModuleNotFoundError`

Activate the virtual environment and install the missing dependency. For
example:

``` bash
python -m pip install psutil pywebview qtpy PyQt6 PyQt6-WebEngine
```

### Desktop notifications do not appear

Confirm that `notify-send` is installed:

``` bash
which notify-send
```

On Ubuntu, install it with:

``` bash
sudo apt install libnotify-bin
```

Also check that desktop notifications are enabled in the Linux desktop
environment.

### The AI assistant returns an error

The monitoring application can still run without the AI assistant. Check
the hosted backend status, provider quota, server logs and secret
configuration separately. Do not put an API key in this public README or
in the client source code.

## Project structure

A typical project directory may look like this:

``` text
smart-server-monitor/
├── client.py
├── requirements.txt
├── monitor_gui.html       # generated at runtime in versions that create it
├── monitor.log            # generated at runtime
└── monitor_data.json      # generated at runtime
```

The optional AI backend may be maintained or deployed separately. Its
source file and deployment entry point depend on the version currently
deployed on the hosting service.

## Project purpose

This project was developed to practise and demonstrate Linux system
monitoring, Python programming, data collection, threshold-based alert
handling, event logging, and the integration of a graphical dashboard
with a Python application.
