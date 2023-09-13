# Poker-profit-tracker-and-analytics
## Introduction
I believe that games are essential in life. Whether you play a casual game of _Ticket to Ride_ or _Pandemic_ a few times a week with family, or you spend your entire weekend meticulously studying textbooks on Bridge or Chess, games are guarunteed to expand your ability to problem-solve, think analytically, develop strategies and - above all - games are a fun way to connect with other human beings, both intellectually and socially.

So, as a student, I felt that it was necessary to join a game society. I attend a reasonably small university (as far as universities go, at least), so there were limited options available to me. My game of choice would have been Backgammon since I was already reasonably familiar with it, but I had to make do with the somewhat more notorious gambling game: Poker. While very different to Backgammon in a number of ways, Poker bears a similar skill-to-luck ratio and need for risk management that I found attractive as someone who enjoys probability and statistics. The only problem was that the minimum buy-ins were £10, and I was a somewhat ~~stingy~~ risk-averse student who couldn't afford to be wasting a tenner every week. (Have you seen the price of jarred pesto in the supermarkets lately?)

Fortunately for me, PokerStars has a "play money" version which is a decent way to practice if your goal is to _not lose all your money_ at a student Poker society. One thing I discovered, however, was the frustrating lack of analytics provided by the platform. Even a very simple and basic measure of play quality such as your PnL over time wasn't immediately available. But what _was_ available to me was all of my hand data in the form of textual accounts of each game.

Being the automation-enthusiast that I am, this was a great opportunity to practice some of my data wrangling skills in Python, and also a bit of SQL as well. The result is that I can now track my PnL, as well as other important Poker play statistics, and have a simple yet comprehensive database from which I can develop more sophisticated analyses in the future.

### TLDR
This project is an exercise in wrangling textual data and constructing a database through which analytics can be performed, demonstrating both my skills in Python and SQL.

## What this repository contains
#### 1. PokerHistoryFiles
These are the textual accounts of a few of the games that I have played. The usernames of all players have been changed to randomly generated ones.
#### 2. Poker_data
This python file is a module containing functions that I have used to extract the relevant information from each hand.
#### 3. Data cleaning
This Jupyter Notebook demonstrates how I wrangled and cleaned the data. The resulting csv files are in the folder called "CSV files".
#### 4. Poker game database creation, usage and analytics
Finally, I can compile my database and see my PnL, as well as some other interesting facts about my opponent's play.


Thank you for reading!
