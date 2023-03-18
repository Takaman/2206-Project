<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Takaman/2206-Project">
    <img src="images/logo-color.png" alt="Logo" width="300" height="300">
  </a>

<h3 align="center">FalseGuardian</h3>

  <p align="center">
    Fake News Detector
    <br />
    <br />
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center">
  
![image](https://user-images.githubusercontent.com/91510432/226091643-2e4fc2a1-7bdb-463b-9479-8de2372c3c38.png)

The FalseGuardian fact checker tool checks your selected text for integrity and truthfulness. 
  
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python-logo]][Python-url]
* [![JavaScript][JavaScript-logo]][JavaScript-url]
* [![Node.js][Node-logo]][Node-url]
* [![npm][npm-logo]][npm-url]
* [![Django][Django-logo]][Django-url]
* [![PyTorch][PyTorch-logo]][PyTorch-url]
* [![spaCy][spaCy-logo]][spaCy-url]
* [![NLTK][NLTK-logo]][NLTK-url]
* [![Hugging Face Transformers][Transformers-logo]][Transformers-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```
  
### Installation and Usage on Windows and Mac
1. Clone the repo
   ```sh
   git clone https://github.com/Takaman/2206-Project.git
   ```
2. Activate VENV and python Dependencies
   ```sh
   cd 2206-Project/djangoserver
   
   # Either create a virtualenv or install dependencies directly
   python -m venv djangoENV
   source djangoENV/bin/activate

   pip install -r requirements.txt
   python -m spacy download en_core_web_lg
   python -m spacy download en_core_web_sm
   ```
3. Run the local Django Server 
   ```sh
   python ./manage.py runserver
   ```
4. Build Chrome Extension and install node.js modules
   ```sh
   cd 2206-Project/FalseGuardian
   npm install
   npm run build 
   or 
   npm run watch 
   ```
   
5. Go to your Chrome Browser's Extension page and load unpacked package

   Navigate to the newly create /build folder
   
    Select the folder

6. Select text to fact check
![image](https://user-images.githubusercontent.com/91510432/226081051-62e905c3-9f15-4ba3-b398-5abba3e59afd.png)
The results would appear at the popup extension. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Takaman/2206-Project.svg?style=for-the-badge
[contributors-url]: https://github.com/Takaman/2206-Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Takaman/2206-Project.svg?style=for-the-badge
[forks-url]: https://github.com/Takaman/2206-Project/network/members
[stars-shield]: https://img.shields.io/github/stars/Takaman/2206-Project.svg?style=for-the-badge
[stars-url]: https://github.com/Takaman/2206-Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/Takaman/2206-Project.svg?style=for-the-badge
[issues-url]: https://github.com/Takaman/2206-Project/issues
[license-shield]: https://img.shields.io/github/license/Takaman/2206-Project.svg?style=for-the-badge
[license-url]: https://github.com/Takaman/2206-Project/blob/master/LICENSE.md
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Django-logo]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[spaCy-logo]: https://img.shields.io/badge/spaCy-2ecc71?style=for-the-badge&logo=spacy&logoColor=white
[spaCy-url]: https://spacy.io/
[NLTK-logo]: https://img.shields.io/badge/NLTK-4c7a6a?style=for-the-badge&logo=ntlk&logoColor=white
[NLTK-url]: https://www.nltk.org/
[Transformers-logo]: https://img.shields.io/badge/Transformers-9769ff?style=for-the-badge&logo=transformers&logoColor=white
[Transformers-url]: https://huggingface.co/transformers/
[Python-logo]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[JavaScript-logo]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Node-logo]: https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white
[Node-url]: https://nodejs.org/
[npm-logo]: https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white
[npm-url]: https://www.npmjs.com/
[PyTorch-url]: https://pytorch.org/
[PyTorch-logo]: https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white
