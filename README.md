# CSE 183 Calendar Project

Design Document w/ screenshots also available here: https://docs.google.com/document/d/1cfnQC7ihEeKunWU8zJE8hmniqjNbU9gRTUZ3KVrYsCQ/edit?usp=sharing

Project Title: Event Calendar

Class: CSE 183, Spring 2023

## Team Members:

Casey Chen | caxchen@ucsc.edu

Bryce Montgomery | bamontgo@ucsc.edu

Daniel Hsieh | dhsieh4@ucsc.edu

Sydney DeHaro | sdeharo@ucsc.edu

Summit Kaushal | sukausha@ucsc.edu

## Description

This project implements an event calendar in which users can create, edit, and delete events that will show up on the selected calendar view on the main 
index page. The user can select from daily, weekly, monthly (default view), and yearly views. Users will be able to create an account, access their own calendar, view the scheduled events for the day/week/month, and search for their scheduled events by name. They will also be able to create/update/delete event details as needed. Users can also send invites to other users which will allow the latter to copy events to their own calendar.


## Main Pages 
- Login page
- Day/week/month/year calendar views
- Event Creation
- Event Edit
- Event Search
- Event Details (title, description, time, date)
- Invite user to event
- View personal event invitations

All pages will be implemented server-side

## Data Organization (databases) 

- User Login Info (email, username, password)
- User Individual Events and Event Data (title, description, time, date)
- User event invitations (sender, recipient, event id)

## User Stories
A user can:

- create an account to keep track of one’s own personal calendar
- create an event with its own unique associated time/date/description
- update event details and delete events as needed
- view personal calendar with a day, week, month, or year view
- click on an event to see its associated title/description/time/date
- send invites to personal events to other users
- accept or decline invites to share an event

## Implementation Plan

<b>Weeks 1-2</b>

Get individual user pages setup, w/ ability to login, view personal monthly calendar page, provide demonstrable website functionality

<b>Weeks 3-4</b>

Weekly and daily views, individual events, user interface improvements, event functionality

<b>Weeks 5-6</b>

Implement additional features such as user invites to allow users to share events
