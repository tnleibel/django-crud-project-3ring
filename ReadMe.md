![3Ring Screenshot](https://i.imgur.com/6iVqNiT.png)

# 3Ring

## INTRO
I remember when I was a kid and collecting pokemon cards was my whole world. Recently I was reminded of that time, and it occurred to me that cards make the perfect CRUD objects! Then when I found out there was a pokemon card API I could incorporate, I was committed to making a website where users can find all of their favorite cards, either modern or vintage, and keep them all in one place where they can be viewed like a virtual three-ring binder of yore. The first thing you'll want to do is create an account, as all actions except search are locked behind a login. To create a card in the DB and add it to your binder, simply search the card you want to find, find the correct card with the correct art in the search results, and hit the button! That card will then appear in your binder page, where it can be viewed with your other cards, or viewed by itself in its details page. Also in the details page, you can add a card to your favorite cards, a set of five cards always displayed above your binder where you can show off your all time favorites.

When you're ready to try it out, head to the [website!]()

Additionally, you can find my planning materials [here!](https://trello.com/b/XVK34WDS/django-crud-app-project)

## ATTRIBUTIONS
I of course must mention and thank https://pokemontcg.io/ for allowing me to use their API to get the card info which is the backbone of this project, none of it would be possible without them.

## TECHNOLOGIES
This project was created using Python, HTML, and CSS for site layout, styling and front-end functionality, as well as Postgresql and Django for backend operations and routing.

## NEXT STEPS 
The first thing I would like to add to the website is a page feature for the search results so the app doesn't fetch every instance of a card from the API all at once. Then I would like to add more field-value pairs to the Card model, as there are quite a few on the card object returned from the API that are not mapped to the Card model when created a new instance. Lastly, I would like do to more work on the styling for the website, including doing more to make the favorite cards section stand out more and fill out the page so there is less empty space.