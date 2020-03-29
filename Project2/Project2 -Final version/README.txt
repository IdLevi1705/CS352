README file
-----------
Name: Idan Levi             NetId: il177
Name: Luis Figueroa-Gil     NetId: lef72

====================================================================
Instructions:
1. simply run ts1.py, ts2.py, ls.py and then client.py files(use terminal -> python <filename.py>).
2. Make sure you enter the follwoing arguments in command line before running each file:
    * python ts1.py <TS1Port>
    * python ts2.py <TS2Port>
    * python ls.py <LSPort> <ts1Hostname> <TS1Port> <ts2Hostname> <TS2Port>
    * python client.py <lsHostname> <LSPort>
3. results will be written to RESOLVED.txt
====================================================================

1. Briefly discuss how you implemented the LS functionality of tracking which TS responded to the query and timing out if neither TS responded.

First, the LS receives the data from the client and forwards them to both TS1 and TS2. Assuming there is no overlapping between DNS tables for each TS server, at most one TS server will respond. A select system call is used to read the DNS tables in each TS server. If the query is in TS1 or TS2, it returns a string in the format hostname IPaddress flag to the client. Otherwise, the select method allows the LS to timeout after 5 seconds and sends an error message to the client.

2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

No.

3. What problems did you face developing code for this project?

4. What did you learn by working on this project?

By working on this project, we learned how important load-balancing servers are in general. When it comes to web servers with a huge amount of traffic, load-balancing servers can distribute properly the load by knowing certain information, such as the DNS configuration, ensuring performance, redundancy, and flexibility. In addition, we learned how to simulate a load-balancing server that receives queries from a client and forwards them to other servers to check whether the queries requested are on the DNS table of each TS server.
