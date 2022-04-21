# F1 Statistics - CI Project 3

![F1 Statistics - Am I Responsive Image](docs/readme_images/responsive.png)

This website was created as a third portfolio project for Code Institute's Diploma in Web Application Development. The site was inspired by my interest in FORMULA 1 as a sport and a desire to have easily accesible information.

The website can be [found here](https://formula-one-statistics.herokuapp.com/).

## Table of Contents

- [Objective](#objective)
- [UX and UI](#ux-and-ui)
  - [Site Owner Goals](#site-owner-goals)
  - [User Stories](#user-stories)
  - [Wireframes](#wireframes)
- [Design](#design)
  - [Background](#background)
  - [Colours](#colours)
  - [Favicon](#favicon)
- [Logic](#logic)
  - [Flowchart](#flowchart)
- [Features](#features)
  - [Home Page](#home-page)
  - [Circuits](#circuits)
  - [Constructors](#constructors)
  - [Drivers](#drivers)
  - [Races](#races)
  - [Seasons](#seasons)
  - [Profile](#profile)
    - [Favourites](#favourites)
    - [Change Password](#change-password)
    - [Delete Account](#delete-account)
  - [Admin Dashboard](#admin-dashboard)
  - [404 Page](#404-page)
- [Deployment](#deployment)
- [Testing](#testing)
  - [Validator Testing](#validator-testing)
  - [Manual Testing](#validator-testing)
- [Credits](#credits)
  - [Languages](#languages)
  - [Frameworks, Libraries and Tools](#frameworks-libraries-and-tools)
  - [Images](#images)

## Objective

#

## UX and UI

- ### Site Owner Goals

  The goal of the site for the owner is to:

  1. Create a home for data from all FORMULA 1 circuits, constructors, drivers, races and seasons.
  2. Allow users to easily navigate the site and allow them to save things to their favourites to allow easy access later.
  3. Have an easy way to add data to the database once an event has finished.

#

- ### User Stories

  - #### First Time Visitor Goals

    1. As a first time user, I want to immediately understand the purpose of the website and how to get started.
    2. As a first time user, I want to be able to easily navigate the site, with a clear indication of which page I am currently on.
    3. As a first time user, I want easy access to external information, where available, to content that I find interesting.

  - #### Returning Visitor Goals

    1. As a returning visitor, I want to be able to access any content I've added to my favourites easily, without needing to search for it directly.
    2. As a returning visitor, I want to be able to manage my account by changing my display name, password or deleting my account entirely.

  #

  ## Wireframes

  The wireframes for this site were created using Balasmiq, with each section and subsection noted.

  The sections below show individual wireframes for different devices, covering the home page when not logged in, the profile page once logged in and a generic overiew of most pages on the site.

   <details>

    <summary>Wireframe - Home & Profile</summary>

  ![Desktop Wireframe Image](docs/wireframes/wireframe_home.png)
    </details>
    <details>

    <summary>Wireframe - Other Pages</summary>

  ![Desktop Wireframe Image](docs/wireframes/wireframe_pages.png)
    </details>

  The directory containing the wireframe images can be found [here](docs/wireframes/).

#

## Logic

- ## Flowchart

     <details>

    <summary>Show Flowchart</summary>

  ![F1 Statistics Flowchart](docs/readme_images/flowchart.png)
    </details>

I spent time thinking about the logic and flow of the site to make sure I had a rough idea of how things were to be laid out and how each part of the site would interact with the database. The flowchart was created using [Lucidchart](https://lucid.app/).

#

## Design

- ## Background

  I made use of the tool available at [SVG Backgrounds](https://www.svgbackgrounds.com/) for this site for a number of reasons.

  - Due to the background being a scalable vector graphic, it will not lose sharpness or quality as the screen size increases and will remain responsive.
  - Due to being an SVG, the file size of the entire background is around 5kb, greatly reducing the total size of the assets required on page load.
  - The tool offers a large amount of customisation and is free for use, as long as attribution is given.
  - The colour of the background chosen has high contrast against the predominantly grey colour scheme of the main game.

- ## Colours

#
  - ![#b71c1c](https://via.placeholder.com/15/b71c1c/000000?text=+) - `#b71c1c` - This colour was chosen for the navbar and footer as a subtle nod to the main colour of the official FORMULA 1 logo.
  - ![#03a9f4](https://via.placeholder.com/15/03a9f4/000000?text=+) - `#03a9f4` - This colour is used for the icons on the main page and was chosen as it contrasts well against the striking red colour of the navbar.
  - ![#01579b](https://via.placeholder.com/15/01579b/000000?text=+) - `#01579b` - This colour was used for the submit buttons at the bottom of the pages for editing drivers & races. This colour was chosen as it contrasts well against the ![#fff](https://via.placeholder.com/15/fff/000000?text=+) white background of the main section, and also against the footer of the page which, as described above, uses the colour ![#b71c1c](https://via.placeholder.com/15/b71c1c/000000?text=+) `#b71c1c`.

  #

  The below colours were not chosen by myself, but are the default colours chosen for the background used from the site [SVG Backgrounds](https://www.svgbackgrounds.com/). I decided to stick with the default colours of the theme chosen due to the close resemblance with the current livery of the [Williams team](https://www.google.com/search?q=Williams+2022+livery&tbm=isch).
  - ![#000022](https://via.placeholder.com/15/000022/000000?text=+) - `#002222`
  - ![#002266](https://via.placeholder.com/15/002266/000000?text=+) - `#002266`
  - ![#001133](https://via.placeholder.com/15/001133/000000?text=+) - `#001133`

#

- ## Favicon

    The website [Favicon.io](https://favicon.io/) was used to generate the favicon image for the website. The chequered flag Unicode emoji , 🏁, was chosen as the icon as it is relative to the theme of the website and is recognisable due to its association with and use in motorsport.

#

# Features

- ## Home Page

  Upon first accessing the site the user is shown the home page which contains 3 main elements.

  - Navbar
    
    The navbar is shown on all pages and is part of the base.html template. The navbar has 3 different configurations.
      
      - If no user session exists the navbar displays the title of the site on the left side, 'F1 Statistics', and links to either 'Login' or 'Register' on the right side. Alternatively, on mobile devices a hamburger menu icon is shown, with a side nav appearing when pressed.
      - If a user session exists, the navbar displays the title of the site on the left side, 'F1 Statistics', and links to all content options and the users profile, as well as the option to log out on the right. Alternatively, on mobile devices a hamburger menu icon is shown, with a side nav appearing when pressed.
      - If the admin user is logged in, the navbar displays the title of the site on the left side, 'F1 Statistics', and links to all content options and access to the admin dashboard, as well as the option to log out on the right. Alternatively, on mobile devices a hamburger menu icon is shown, with a side nav appearing when pressed.

- ## Circuits

- ## Constructors

- ## Drivers

- ## Races

- ## Seasons

- ## Profile

  - ### Favourites
  - ### Change Password
  - ### Delete Account

- ## Admin Dashboard

- ## 404 Page

#

## Deployment

This project was created using GitHub and hosted on the Heroku Platform.

The following steps were taken to deploy the project:

    1. Login to the Heroku website, or create an account if you don't already have one.
    2. After you have logged in, click on 'New' in the top right of the screen and select 'Create New App'
    3. Enter a name for your app(This name MUST be unique). Heroku will display a warning if your chosen name has already been taken.
    4. Choose the region in which you would like your app to be hosted.
    5. Go to the Settings tab and go to "Config Vars", and then select "Reveal Config Vars"
    6. Enter PORT into the KEY field and 8000 into the value, then click "Add".
    7. Add any other relevant Config Vars to this section by repeating Step 6.
    8. Navigate to the "Deploy" tab, and select Github as the deployment method
    9. Log in to Github and select the repository you wish to link with Heroku.
    10. You can choose between two deployment options for your app.
      - Automatic will re-deploy your app when changes are made to the linked repository, or you will be notified if the deployment has failed.
      - Manual deployment requires you to log in to Heroku and select the "Deploy" button when any changes have been made.
    11. Once these steps have been followed your app will be built and deployed.
      - If successful you will be provided a link to the live page.
      - If not successful, the build will fail and the activity log will provide more information about the issue.

#

## Testing

- ## Manual Testing

  <details>
    <summary>CSS Validation</summary>

  CSS was validated using [The W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/validator). A full report can be viewed [here](docs/readme_images/CSS_Validation/css_validator_full.png).

  ![CSS Validation](docs/readme_images/CSS_Validation/css_validator.png)

  </details>
  <details>
    <summary>HTML Validation</summary>

  HTML was validated using [The W3C Nu Html Checker](https://validator.w3.org/nu/). All pages were checked using this tool and most screens have been captured and can be viewed [here](docs/readme_images/HTML_Validation/). Some pages have not been captured due to the large number of lines contained on certain pages.

  ![CSS Validation](docs/readme_images/CSS_Validation/css_validator.png)

  </details>

    </details>
  <details>
    <summary>JS / Jquery Validation</summary>

  Javascript/JQuery was validated using [JSHint](https://jshint.com/). Three warnings were returned, but all contained the same information regarding the use of 'let'. As ES6 is the version being used, these warnings were disregarded.

  ![JSHint Warnings](docs/readme_images/jshint.png)

  </details>

#

- ## Lighthouse Testing

#

- ## Wave Testing

  All pages on the site were tested using the [WAVE Web Accessibility Evaluation Tool](https://wave.webaim.org/). All pages returned **0 errors**, **0 contrast errors**. A single Alert was returned on the Login page advising of a redundant link, but I believe this is not valid.

  Due to the number of pages contained on the site, I have not linked the images within this repository, but the site can be explored on the WAVE tool by clicking [this link](https://wave.webaim.org/report#/https://formula-one-statistics.herokuapp.com/).

  ![Wave Example](docs/readme_images/wave.png)

#

## Credits

- ## Languages and Frameworks

  - [HTML5](https://en.wikipedia.org/wiki/HTML5)
  - [CSS](https://en.wikipedia.org/wiki/CSS)
  - [Flask](https://flask.palletsprojects.com/en/2.1.x/)
  - [Javascript](https://en.wikipedia.org/wiki/JavaScript)
  - [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
  - [JQuery](https://en.wikipedia.org/wiki/JQuery)
  - [Materialize](https://materializecss.com/)
  - [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>)

- ## Libraries and Tools

  - [Am I Responsive](http://ami.responsivedesign.is/) - Used to verify responsiveness of website on different devices.
  - [Balsamiq](https://balsamiq.com/) - Used to generate Wireframe images.
  - [Browser Stack](https://www.browserstack.com/) - Used for Cross Site Browser Testing.
  - [Chrome Dev Tools](https://developer.chrome.com/docs/devtools/) - Used for overall development and tweaking, including testing responsiveness and performance.
  - [DataTables](https://datatables.net/) - A JQuery tool to allow pagination and searching functionality to be added to tables easily.
  - [Favicon.io](https://favicon.io) - Used to generate Favicon image.
  - [Font Awesome](https://fontawesome.com/) - Used for icons on multiple pages.
  - [Flag Icons](https://github.com/lipis/flag-icons) - Repo created by [Lipis](https://github.com/lipis) containing SVG images of all country flags.
  - [GitHub](https://github.com/) - Used for version control.
  - [Heroku](https://heroku.com) - Used for deployment and hosting of the project.
  - [JQuery](https://en.wikipedia.org/wiki/JQuery) - Used to simplify definition of DOM elements, but used minimally with a preference for vanilla Javascript.
  - [JSHint](https://jshint.com/about/) - Linter used to flag errors, bugs and warnings.
  - [LucidChart](https://lucid.app/) - Used to create the flowchart for this site.
  - [PEP8Online](http://pep8online.com/) - Tool used to ensure app.py is PEP8 compliant.
  - [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) - Used for consistent code formatting.
  - [Slack](https://slack.com/) - Used for support and advice from the Code Insitute Community.
  - [SVG Backgrounds](https://www.svgbackgrounds.com/) - Used to style the background for the site due to low file size and responsiveness. Licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  - [Visual Studio Code](https://code.visualstudio.com/) - Application used for development of this site.
  - [W3C](https://www.w3.org/) - Used for HTML & CSS Validation.
  - [WAVE](https://wave.webaim.org/) - Used for Accessibility evaluation.
  - [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) - This API was used to obtain images of drivers and constructors directly from the relevant Wikipedia page.

- ## Images

  The emoji graphic used for the favicon is from the open source project [Twemoji](https://twemoji.twitter.com/). The graphics are copyright 2020 Twitter, Inc and other contributors. The graphics are licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).

  The [404 - Page Not Found](static/img/404.jpg) image was created by, and used with permission from, Reddit user [heyitsalex85](https://www.reddit.com/user/heyitsalex85/).
