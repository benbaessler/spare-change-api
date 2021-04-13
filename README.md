# spare-change-donator

An application for automatically donating spare change from Stripe purchases.

## Process:
1. The user makes a purchase.
2. A webhook is sent to the server.
3. The application charges the user with the left-over change.

*Built using Stripe API*
