![](assets/logo.png)

# MaPS Auth Server
  
Authentication API server for [MaPS (https://github.com/aaruni96/maps)](https://github.com/aaruni96/maps)

# Table of Contents

- [About the Project](#about-the-project)
  * [Tech Stack](#tech-stack)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Installation](#installation)
- [License](#license)
- [Contact](#contact)
  

## About the Project

[MaPS](https://github.com/aaruni/maps) uses the TUS server (tusd) to implement resumable uploads.
tusd allows hooking into arbitrary scripts during various phases of the upload process for
additional control. This project provides a script for the `pre-hook`, which issues a go/no-go
status for an attempted upload. Upon failure, no information except `Authentication Failed` is
returned.

<!-- TechStack -->
### Tech Stack

#### Upload Server
- [TUS Server](https://tus.github.io/tusd/)

#### Programming Language
- Python

<!-- Features -->
### Features

- Register users allowed to upload
- Prunes users out of the database after 48 hours
- Checks incoming upload against user database


<!-- Getting Started -->
## Getting Started


<!-- Installation -->
### Installation

Copy `src/maps-auth.py` to `pre-create` in your tusd hooks directory, and register some users.
tusd will automatically hook into this script and check for authentication before uploads.


<!-- License -->
## License

Distributed under the AGPLv3-or-later. See [LICENSE](LICENSE) for more information.


<!-- Contact -->
## Contact

Aaruni Kaushik - akaushik@mathematik.uni-kl.de
