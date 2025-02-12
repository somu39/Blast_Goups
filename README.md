# Houdini Group Blast Tool

A custom Houdini tool for blasting geometry groups with a sleek, dark-themed interface built using PySide2. This tool streamlines the process of selecting and blasting groups from a Houdini geometry node, complete with advanced UI features and automatic node creation with color gradients.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

The Houdini Group Blast Tool is designed to simplify the process of creating blast nodes for selected geometry groups within Houdini. With its custom-built user interface, the tool allows you to:

- View and select point and primitive groups from a Houdini node.
- Invert your selection to blast all groups except those selected.
- Automatically generate blast nodes with a visually distinct color gradient for easy identification.
- Auto-refresh the group list based on the current Houdini node selection.

This tool is particularly useful for artists and technical directors who work with complex geometries and need to quickly isolate and manipulate specific groups.

---

## Features

- **Custom Dark Theme UI**: Enjoy a modern, dark-themed interface with a comprehensive stylesheet.
- **Group Selection Dialog**: Automatically populates with available point and primitive groups from the selected node.
- **Invert Selection Option**: Easily switch between blasting selected groups or their inverse.
- **Select All Option**: A checkbox to quickly select or deselect all available groups.
- **Blast Node Creation**: Automatically creates blast nodes for each selected group, setting the proper parameters.
- **Color Gradient Application**: Applies a gradient to the blast nodes to visually differentiate between groups.
- **Auto Refresh**: The UI refreshes in real-time, ensuring that the list of groups reflects the current node selection.

---

## Installation

### Prerequisites

- **Houdini**: Ensure that you have Houdini installed (Houdini 18 or later is recommended).
- **PySide2**: Houdini comes with PySide2 by default, but verify it is available in your Houdini Python environment.

### Steps

1. **Clone or Download the Repository**

   ```bash
   https://github.com/somu39/Blast_Goups.git
   
