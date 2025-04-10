# CS411ProjectS24

## Project Complete!

There were some issues implementing Firebase, so the login and profile implementation, while fully functional, is not as pretty to look at as the rest of this website. They deliver everything that was promised in the original proposal, though, so this is simply an aesthetic issue. The website interacts with 5 years of Boston 311 data, which is an expansion on the proposed functionality, to ensure users do not miss any relevant information. For testing purposes, it is best to use addresses with a history of complaints -- for example 418 Ashmont St Dorchester MA 02124, which reported a Rat Bite in 2023, or 186 Marlborough St Boston MA 02116, which reported unsatisfactory living conditions.

## UPDATE: Proposed Timeline

### Backend
1. Input Management:
- Convert street address to lattitude/longitude using a map service
2. API Management:
- Search for all entries in database within 6 city blocks of the given address (one city block ~1/12 km, there are 111 km in one line of lattitude/longitude. Therefore a six block radius is 0.0045 degrees latitude/longitude)
- Filter out irrelevant categories (relevent categories listed below)
- Caculate rating
3. Profile
- Implement OAuth sign in
- Keep track of a database of user info

### Frontend
1. Input location that takes street addresses as user input
2. Menu to view all past entries and their ratings
3. Profile editor and login

## Proposal 1: Apartment Selector

Our first proposed project will use [Boston 311 data](https://data.boston.gov/dataset/311-service-requests/resource/e6013a93-1321-4f2a-bf91-8d8a02f1e62f) from 2023 to assign ratings to user-entered apartments, in order to make the renting process easier. Each user will have a profile which saves a User ID and the addresses and rating of all of the apartments they have entered into the application. It will display the best and most recent apartment that a given user has entered.

In order to calculate this rating, we will use a variety of types of 311 data. They are semi-ranked as follows: squalid living conditions, poor conditions of property, unsatisfactory living conditions, no utilities(electricity, gas, water), chronic dampness or mold, heat - excessive insufficient, mice infestation, pest infestation, maintinence complaint, noise disturbance (automotive, dumpster and loading), loud parties/music/people, student overcrowding, sewage/septic back up, and unshoveled sidewalk. These complaint types are all contained in a single database, so should be relatively easy to access all at once, but if for any reason this list becomes too lengthy we will shorten it accordingly.

The user will be asked to enter the address of the apartment they are considering. The application will then filter through all of the data that fulfills the above type requirements on a radius of around 900 ft (approximately one city block). It is possible that instead we will group the types of data into distance-based groupings. Regardless, once the data has filtered, a rating will be calculated based on the number of hits and their weight, which we will assign to each type, and then displayed to the user.

The tech stack for this project will include a javascript front end, Python back end, SQL queries, OAuth log-in, and (of course) a github repository.
