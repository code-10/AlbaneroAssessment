# AlbaneroAssessment
Albanero Train System

Albanero Train Ticketing System
1. Guest Users can view Train Schedules.
2. Only Registered/LoggedIn (Email, Password) Users can Book a Ticket.
3. User can select Source, Destination and Date for get Train Schedules
4. Train Schedule will have Train Number, Train Name, Departure, Arrival, Time Taken, Available Seats in General and Tatkal 
5. If all seats are booked, tickets will be moved to waiting list

Note: 
1. User cannot select past data while searching for train schedules 
2. One user cannot book more than 6 tickets
3. Source and Destination cannot be same
4. Priority in Waiting List is given by time of the ticket booked in milliseconds
5. If the available seats are 3 and waiting list user has 4 passengers, then the next available user is given priority
6. Cancellation Window is 3 hours for General and 2 hours for Tatkal
