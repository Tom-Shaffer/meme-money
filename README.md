# meme-money
  
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
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]




<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Tom-Shaffer/meme-money">
    <img src="https://c4.wallpaperflare.com/wallpaper/864/120/856/futurama-philip-j-fry-memes-money-wallpaper-preview.jpg" alt="Logo" width="728" height="455">
  </a>

<h3 align="center">meme-money</h3>

  <p align="center">
    Remember to invest wisely, and always stick to the fundamentals. I do not recommend using this tool for real investing.

This python project allows for stock analytics to be collected from the r/WallStreetBets subreddit
by searching for specific upper-case symbols in posts and comments. No API keys required, go ahead and downoad the project and run the meme-money.py to get started!
    <br />
    <a href="https://github.com/Tom-Shaffer/meme-money"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Tom-Shaffer/meme-money">View Demo</a>
    ·
    <a href="https://github.com/Tom-Shaffer/meme-money/issues">Report Bug</a>
    ·
    <a href="https://github.com/Tom-Shaffer/meme-money/issues">Request Feature</a>
  </p>
</div>

### Built With

* [Python3](https://www.python.org)


<!-- USAGE EXAMPLES -->
## Usage

Quite simply provide a positive integer of days when prompted, and meme-money.py will parse reddit that number of days into the past. By default, it will use the supplied version of searchdata.tsv, which hosts a list of around 6,000 stock market tickers from stock exchanges around the world.

If you would like, upload your own searchdata.tsv file with any number of fields. meme-money.py will look for symbols matching the uppercase of all elements in the first column, and aggregate them based on how many "hits" it finds on https://www.reddit.com/r/wallstreetbets/, and then supply all the ancillary columns that were provided as well.

<img width="791" alt="Screen Shot 2022-02-06 at 8 23 27 PM" src="https://user-images.githubusercontent.com/54244645/152715508-807dff35-534d-4893-920f-a854db8f8cbe.png">

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Tom-Shaffer/meme-money](https://github.com/Tom-Shaffer/meme-money)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Tom-Shaffer/meme-money.svg?style=for-the-badge
[contributors-url]: https://github.com/Tom-Shaffer/meme-money/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Tom-Shaffer/meme-money.svg?style=for-the-badge
[forks-url]: https://github.com/Tom-Shaffer/meme-money/network/members
[stars-shield]: https://img.shields.io/github/stars/Tom-Shaffer/meme-money.svg?style=for-the-badge
[stars-url]: https://github.com/Tom-Shaffer/meme-money/stargazers
[issues-shield]: https://img.shields.io/github/issues/Tom-Shaffer/meme-money.svg?style=for-the-badge
[issues-url]: https://github.com/Tom-Shaffer/meme-money/issues
[license-shield]: https://img.shields.io/github/license/Tom-Shaffer/meme-money.svg?style=for-the-badge
[license-url]: https://github.com/Tom-Shaffer/meme-money/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/tom-scott-shaffer/
