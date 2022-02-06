<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

![build passing](https://github.com/joeyshuttleworth/NumbaIDA/actions/workflows/install_and_run.yml/badge.svg)

[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<h3 align="center">NumbaIDA</h3>

  <p align="center">
    <br />
    <br />
    <br />    
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#known-issues">Known Issues</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--- [![Product Name Screen Shot][product-screenshot]](https://example.com) --->

NumbaIDA is a Python package allowing you to quickly solve Differential Algebraic Equation (DAE) problems in Numba JIT compiled functions using the LLNL SUNDIALS IDA solver. The code borrows heavilty from [NumbdaLSODA](https://github.com/Nicholaswogan/NumbaLSODA) but uses IDA instead of LSODA (thank you!)

DAEs may be thought of a a system of ordinary differential equations (ODEs) with some additional constraints. For example, consider the linear sytem

dx/dt = - a * x + b * y,

dy/dt = - b * y + a * x

with the constaint x + y = 1. In this case, you can rewrite the equation for dx/dt so that it doesn't include any y terms. Alternatively, you can use a solver such as IDA to solve this as a DAE problem. NumbaIDA allows you to use the IDA solver in Python as a JIT compiled function using Numba.

### Built With

* [Numpy](https://numpy.org/)
* [Numba](https://numba.pydata.org/)
* [SUNDIALS](https://computing.llnl.gov/projects/sundials)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The `examples` directory shows example(s) of how to input a DAE problem into NumbaIDA. 

### Prerequisites

In order to install NumbaIDA you require a number of commonly used utility programs for building software. On Ubuntu/Debian these may be easily installed by running:
```
sudo apt-get update
sudo apt-get install -y gcc cmake build-essential clang-tidy python3
```

Next, install 'pip' and 'venv' with:
```
        python3 -m pip install --upgrade pip
        python3 -m pip install --upgrade venv
```


### Installation

It is reccomended to install and run 'NumbaIDA' a virtual environment. This can be done by navigating to the root directory (NumbaIDA/ by default) and running:

```
        python3 -m pip install --upgrade venv
        python3 -m venv .venv
        activate .venv/bin/activate
```


Next install scikit-build into the virtual environment:
 ```
 python3 -m pip install scikit-build
 ```
 
 Finally, install `NumbaIDA` with
```
pip install .
```


<!-- USAGE EXAMPLES -->
<!---
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>
--->

<!-- Known Issues -->
## Known Issues
1. It is not currently possible to specify a jacobian
2. `ida_wrapper` is not thread safe! 
3. SUNDIALS is very flexible and allows a number of linear and nonlinear solvers to be used -- currently it is only possible to use the defaults.
4. Currently, only dense matrices/vectors may be used 
5. IT is not yet possible to use one of SUNDIAL's root-finders during the residual calculation


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License
See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


SUNDIALS is distributed under the BSD 3-Clause License:

Copyright (c) 2002-2022, Lawrence Livermore National Security and Southern Methodist University.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Nicholaswogan's NumbaLSODA package](https://github.com/Nicholaswogan/NumbaLSODA) which this package is _heavily_ based on
* [SUNDIALS](https://github.com/LLNL/sundials)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/joeyshuttleworth/NumbaIDA/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
